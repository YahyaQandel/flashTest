from decimal import Decimal
from moneyed.classes import CURRENCIES, EGP, Money
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from datetime import date, datetime, timedelta

from user.models import User
from money.models import MoneyUploaded, Transaction
from money.serializer import MoneyRequestSerializer,TransferRequestSerializer
from user.serializer import UserSerializer
import moneyed
from bank.views import  is_user_connected_to_bank
from .config_parser import Config

DAILY_LIMIT = 10000
WEEKLY_LIMIT = 50000
config = Config()

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

        if amount_to_be_uploaded > config.get_daily_limit():
                return Response(
                    data={"error": "Maximum amount to be uploaded 9999"},
                    status=status.HTTP_400_BAD_REQUEST)

        total_amount_uploaded_today = self.get_total_amount_uploaded_in(request.user, date.today())
        if total_amount_uploaded_today + amount_to_be_uploaded > config.get_daily_limit():
            return Response(
                data={"error": "You have exceeded your daily limit ({}) for ({})".format(config.get_daily_limit(),date.today())},
                status=status.HTTP_400_BAD_REQUEST)
        total_amount_uploaded_current_week = self.get_total_amount_uploaded_in_current_week(request.user)
        if total_amount_uploaded_current_week > config.get_weekly_limit():
            return Response(
                data={"error": 'You have exceeded your weekly limit ({})'.format(config.get_weekly_limit())},
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
        is_valid_params, response = User.serialize_params(request)
        if not is_valid_params:
            return response
        user_params = response
        amount_to_be_transfered = Decimal(request.data['amount'])
        if amount_to_be_transfered > config.get_daily_limit():
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
        if total_amount_transferred_today + amount_to_be_transfered > config.get_daily_limit():
            return Response(
                data={"error": "You have exceeded your daily transfer limit ({}) for ({})".format(config.get_daily_limit(),date.today())},
                status=status.HTTP_400_BAD_REQUEST)
        total_amount_uploaded_current_week = self.get_total_amount_transferred_in_current_week(request.user)
        if total_amount_uploaded_current_week > config.get_weekly_limit():
            return Response(
                data={"error": 'You have exceeded your weekly transfer limit ({})'.format(config.get_weekly_limit())},
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