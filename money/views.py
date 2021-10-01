from decimal import Decimal
from moneyed.classes import EGP
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from datetime import date, datetime, timedelta

from user.models import User
from money.models import MoneyUploaded
from money.serializer import MoneyRequestSerializer
from user.serializer import UserSerializer
import moneyed
from bank.models import Bank
from bank.views import  is_user_connected_to_bank

DAILY_LIMIT = 10000
WEEKLY_LIMIT = 50000
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

        total_amount_uploaded_today = self.get_total_amount_uploaded_in(date.today())
        if total_amount_uploaded_today + amount_to_be_uploaded > DAILY_LIMIT:
            return Response(
                data={"error": "You have exceeded your daily limit (10k) for ({})".format(date.today())},
                status=status.HTTP_400_BAD_REQUEST)
        total_amount_uploaded_current_week = self.get_total_amount_uploaded_in_current_week()
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

    def get_total_amount_uploaded_in(self, required_day):
        money_uploaded_today = None
        day_before = required_day - timedelta(days=1)
        try:
            money_uploaded_today = MoneyUploaded.objects.filter(created_at__gt=day_before, created_at__lte= required_day)
        except MoneyUploaded.DoesNotExist:
            pass
        total_amount_uploaded_today = 0
        if money_uploaded_today:
            for one_time_upload in money_uploaded_today:
                total_amount_uploaded_today += one_time_upload.amount.amount
        return total_amount_uploaded_today

    def get_total_amount_uploaded_in_current_week(self):
        today = datetime.today()
        total_amount_uploaded_current_week = 0
        for i in range(1, 8):
            day = today - timedelta(days=i)
            day_amount = self.get_total_amount_uploaded_in(day)
            total_amount_uploaded_current_week += day_amount

        return total_amount_uploaded_current_week