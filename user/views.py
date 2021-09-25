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
from user.serializer import LoginRequestSerializer, ResponseSerializer, MoneyRequestSerializer, UserSerializer
import moneyed
import re   

class Login(APIView):
    class_serializer = LoginRequestSerializer

    def post(self, request, format=None):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user_password = request.data['password']
            if "username" in request.data:
                username = request.data['username']
                user = User.objects.get(username=username)
            elif "email" in request.data:
                user_email = request.data['email']
                user = User.objects.get(email=user_email)
            else:
                return Response(
                    data={"detail": "either provide your email or your username"},
                    status=status.HTTP_401_UNAUTHORIZED)
            if not user.check_password(user_password):
                return Response(
                    data={"detail": "The user credentials were incorrect."},
                    status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response(data={"detail": "The user credentials were incorrect."},
                            status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data=ResponseSerializer(user).data, status=status.HTTP_200_OK)


DAILY_LIMIT = 10000
WEEKLY_LIMIT = 50000
class Money(APIView):
    class_serializer = MoneyRequestSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def post(self, request, format=None):
        serializer = MoneyRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount_to_be_uploaded = Decimal(request.data['amount'])

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
            # print("day:{}-amount:{}".format(day, day_amount))
        # print(total_amount_uploaded_current_week)
        return total_amount_uploaded_current_week