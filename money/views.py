from decimal import Decimal
from django.contrib.sessions.models import Session
from django.db.models import base
from moneyed.classes import CURRENCIES, EGP, Money
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from user.views import validate_login_request_params

from datetime import date, datetime, timedelta

from user.models import User
from money.models import MoneyUploaded,Transaction
from money.serializer import MoneyRequestSerializer, TransferRequestSerializer, CurrencyExchangeSerializer
from user.serializer import UserSerializer
import moneyed
from bank.models import Bank
from bank.views import  is_user_connected_to_bank
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect
from bank.views import get_logged_in_user
import requests
from django.conf import settings

DAILY_LIMIT = 10000
WEEKLY_LIMIT = 50000

class CurrencyExchange(APIView):
    CURRS = ['USD', 'AUD', 'CAD','PLN', 'MXN', 'EUR', 'EGP']
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'currency_exchange.html'
    class_serializer = CurrencyExchangeSerializer

    def get(self, request):
        if request.session.session_key:
            try:
                user = get_logged_in_user(request)
            except Session.DoesNotExist:
                return redirect(to="/login")
            default_base_cur = 'EUR'
            rates = self.get_currenceis_rate(default_base_cur)
            new_balance_in_default_rate = self.get_user_balance_in_currency(user,default_base_cur)
            response_data = {'rates': rates,
                            'balance' : new_balance_in_default_rate,
                            'currencies': CURRENCIES,
                            'base_curr': default_base_cur}

            return Response(response_data)
        else:
            return redirect(to="/login")

    def post(self, request):
        if request.session.session_key:
            user = get_logged_in_user(request)
        else:
            return redirect(to="/login")
        serializer = CurrencyExchangeSerializer(data=request.data)
        is_valid_params = serializer.is_valid(raise_exception=False)
        if not is_valid_params:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        base_currency = request.data['currency']
        rates = self.get_currenceis_rate (base_currency)
        user_currency = str(user.balance.currency)
        new_balance_in_default_rate = round(float(user.balance.amount ) * float(rates[user_currency]), 2)
        return Response({'balance': new_balance_in_default_rate,'rates': rates,'currencies': CURRENCIES, 'base_curr': base_currency})

    def get_currenceis_rate(self, base_currency):
        ploads = {'access_key': settings.CURRENCIES_KEY}
        api_url = "{}".format(settings.CURRENCIES_API)
        r = requests.get(api_url, params=ploads)
        currencies_rates_response = r.json()
        rates = currencies_rates_response['rates']
        response_rates = {}
        exchange_rate = 1 * rates[base_currency]
        for key, value in rates.items():
            response_rates[key] = round(rates[key] / exchange_rate, 5)
        return response_rates

    def get_user_balance_in_currency(self, user, currency):
        rates = self.get_currenceis_rate(currency)
        user_currency = str(user.balance.currency)
        return round(float(user.balance.amount ) * float(rates[user_currency]), 2)

class Upload(APIView):
    class_serializer = MoneyRequestSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def post(self, request, format=None):
        serializer = MoneyRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount_to_be_uploaded = Decimal(request.data['amount'])

        if not is_user_connected_to_bank(request.user):
            return Response(
                    data={"error": "user doesnt have a bank account connected"},
                    status=status.HTTP_400_BAD_REQUEST)

        if amount_to_be_uploaded > DAILY_LIMIT:
                return Response(
                    data={"error": "Maximum amount to be uploaded 9999"},
                    status=status.HTTP_400_BAD_REQUEST)

        total_amount_uploaded_today = self.get_total_amount_uploaded_in(request.user, date.today())
        if total_amount_uploaded_today + amount_to_be_uploaded > DAILY_LIMIT:
            return Response(
                data={"error": "You have exceeded your daily limit (10k) for ({})".format(date.today())},
                status=status.HTTP_400_BAD_REQUEST)
        total_amount_uploaded_current_week = self.get_total_amount_uploaded_in_current_week(request.user)
        if total_amount_uploaded_current_week > WEEKLY_LIMIT:
            return Response(
                data={"error": 'You have exceeded your weekly limit (50k)'},
                status=status.HTTP_400_BAD_REQUEST)
        money_uploaded_now = MoneyUploaded(user=request.user,amount= amount_to_be_uploaded)
        money_uploaded_now.save()
        user = User.objects.get(email=request.user.email)
        new_balance = amount_to_be_uploaded + user.balance.amount
        user.balance = moneyed.Money(amount=new_balance, currency="EGP")
        user.save()
        return Response(data=UserSerializer(user).data, status=status.HTTP_200_OK)

    def get_total_amount_uploaded_in(self, user, required_day):
        money_uploaded_today = None
        day_before = required_day - timedelta(days=1)
        try:
            money_uploaded_today = MoneyUploaded.objects.filter(user=user,created_at__gt=day_before, created_at__lte= required_day)
        except MoneyUploaded.DoesNotExist:
            pass
        total_amount_uploaded_today = 0
        if money_uploaded_today:
            for one_time_upload in money_uploaded_today:
                total_amount_uploaded_today += one_time_upload.amount.amount
        return total_amount_uploaded_today

    def get_total_amount_uploaded_in_current_week(self, user):
        today = datetime.today()
        total_amount_uploaded_current_week = 0
        for i in range(1, 8):
            day = today - timedelta(days=i)
            day_amount = self.get_total_amount_uploaded_in(user, day)
            total_amount_uploaded_current_week += day_amount

        return total_amount_uploaded_current_week


class Transfer(APIView):
    class_serializer = TransferRequestSerializer
    permission_classes = (
        IsAuthenticated,
    )
    def post(self, request):
        serializer = TransferRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_valid_params, response = validate_login_request_params(request)
        if not is_valid_params:
            return response
        user_params = response
        amount_to_be_transfered = Decimal(request.data['amount'])
        if amount_to_be_transfered > DAILY_LIMIT:
                return Response(
                    data={"error": "Maximum amount to be transferred 9999"},
                    status=status.HTTP_400_BAD_REQUEST)
        try:
            sender = request.user
            recipient = User.objects.get(**user_params)
            if not recipient:
                return Response(data={'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response(data={'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        if sender.balance.amount < amount_to_be_transfered:
            return Response(data={'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
        transaction = Transaction(sender=sender, amount=amount_to_be_transfered, 
                                                recipient=recipient)

        total_amount_transferred_today = self.get_total_amount_transferred_in(sender, date.today())
        if total_amount_transferred_today + amount_to_be_transfered > DAILY_LIMIT:
            return Response(
                data={"error": "You have exceeded your daily transfer limit (10k) for ({})".format(date.today())},
                status=status.HTTP_400_BAD_REQUEST)
        total_amount_uploaded_current_week = self.get_total_amount_transferred_in_current_week(request.user)
        if total_amount_uploaded_current_week > WEEKLY_LIMIT:
            return Response(
                data={"error": 'You have exceeded your weekly transfer limit (50k)'},
                status=status.HTTP_400_BAD_REQUEST)
        transaction.save()
        sender.balance = Money(amount=(sender.balance.amount - amount_to_be_transfered))
        sender.save()
        recipient.balance = Money(amount=(recipient.balance.amount + amount_to_be_transfered))
        recipient.save()
        return Response(data=UserSerializer(sender).data, status=status.HTTP_200_OK)

    def get_total_amount_transferred_in(self, user, required_day):
        money_transferred_today = None
        day_before = required_day - timedelta(days=1)
        try:
            money_transferred_today = Transaction.objects.filter(sender=user, created_at__gt=day_before, created_at__lte= required_day)
        except Transaction.DoesNotExist:
            pass
        total_amount_transferred_today = 0
        if money_transferred_today:
            for one_time_upload in money_transferred_today:
                total_amount_transferred_today += one_time_upload.amount.amount
        return total_amount_transferred_today

    def get_total_amount_transferred_in_current_week(self, user):
        today = datetime.today()
        total_amount_uploaded_current_week = 0
        for i in range(1, 8):
            day = today - timedelta(days=i)
            day_amount = self.get_total_amount_transferred_in(user, day)
            total_amount_uploaded_current_week += day_amount

        return total_amount_uploaded_current_week