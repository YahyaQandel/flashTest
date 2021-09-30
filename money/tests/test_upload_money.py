from django.test import TestCase
from rest_framework.test import APIClient
from user.factories import UserFactory
from rest_framework.authtoken.models import Token
from user.models import User
from decimal import Decimal
from datetime import date, datetime, timedelta
from money.models import MoneyUploaded
import moneyed

TOKEN_TYPE = 'Bearer'
UPLOAD_MONEY_URL = "/api/v1/money/upload"


def get_request_authentication_headers(user):
    user_token = Token.objects.get(user_id=user.id)
    request_headers = {'HTTP_AUTHORIZATION': '{} {}'.format(TOKEN_TYPE, user_token)}
    return request_headers

# Create your tests here.


class TestMoneyUpload(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.user = UserFactory()
        self.request_headers = get_request_authentication_headers(self.user)
        self.amount_to_be_uploaded = 0

    def testUploadInvalidMoneyValue(self):
        request_data = {"amount": "f"}
        response = self.api_client.post(UPLOAD_MONEY_URL, data=request_data, **self.request_headers)
        response_data = response.json()
        self.assertEquals(response.status_code, 400)
        self.assertIn('amount', response_data)
        self.assertIn('A valid number is required.', response_data['amount'])

    def testUploadNegativeOrZeroMoneyValue(self):
        request_data = {"amount": Decimal(-15)}
        self.amount_to_be_uploaded = request_data['amount']
        response = self.api_client.post(UPLOAD_MONEY_URL, data=request_data, **self.request_headers)
        response_data = response.json()
        self.assertEquals(response.status_code, 400)
        self.assertIn('Ensure this value is greater than or equal to 1.0.', response_data['amount'])
        request_data = {"amount": Decimal(0)}
        response = self.api_client.post(UPLOAD_MONEY_URL, data=request_data, **self.request_headers)
        response_data = response.json()
        self.assertEquals(response.status_code, 400)
        self.assertIn('Ensure this value is greater than or equal to 1.0.', response_data['amount'])

    def testUploadMoneyExceedWeeklyLimit(self):
        request_data = {"amount": Decimal(7000)}
        self.amount_to_be_uploaded = request_data['amount']
        today = datetime.today()
        daily_amount = 7500
        for i in range(1, 10):
            day_before = today - timedelta(days=i)
            day_before_upload_money_obj = MoneyUploaded(user=self.user, amount=daily_amount + i*10)
            day_before_upload_money_obj.save()
            day_before_upload_money_obj.created_at = day_before.date()
            day_before_upload_money_obj.save()
            self.user.balance = moneyed.Money(amount=daily_amount, currency='EGP') + self.user.balance
            self.user.save()
        user_old_balance = self.user.balance.amount
        response = self.api_client.post(UPLOAD_MONEY_URL, data=request_data, **self.request_headers)
        response_data = response.json()
        self.assertEquals(response.status_code, 400)
        self.assertEqual(self.user.balance.amount, user_old_balance)
        self.assertIn('You have exceeded your weekly limit (50k)'.format(date.today()), response_data['error'])

    def testUploadMoneyNotExceedingWeeklyLimit(self):
        request_data = {"amount": Decimal(100)}
        self.amount_to_be_uploaded = request_data['amount']
        today = datetime.today()
        daily_amount = 2000
        for i in range(1, 10):
            day_before = today - timedelta(days=i)
            day_before_upload_money_obj = MoneyUploaded(user=self.user, amount=daily_amount + i*10)
            day_before_upload_money_obj.save()
            day_before_upload_money_obj.created_at = day_before.date()
            day_before_upload_money_obj.save()
            self.user.balance = moneyed.Money(amount=daily_amount, currency='EGP') + self.user.balance
            self.user.save()
        user_old_balance = self.user.balance.amount
        response = self.api_client.post(UPLOAD_MONEY_URL, data=request_data, **self.request_headers)
        self.user = User.objects.get(email=self.user.email)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(self.user.balance.amount, user_old_balance + request_data['amount'])
        
    def testUploadMoneyExceedDailyLimit(self):
        user_old_balance = self.user.balance.amount
        request_data = {"amount": Decimal(9900)}
        self.amount_to_be_uploaded = request_data['amount']
        response = self.api_client.post(UPLOAD_MONEY_URL, data=request_data, **self.request_headers)
        self.assertEquals(response.status_code, 200)
        request_data = {"amount": Decimal(200)}
        response = self.api_client.post(UPLOAD_MONEY_URL, data=request_data, **self.request_headers)
        response_data = response.json()
        self.assertEquals(response.status_code, 400)
        self.assertEqual(self.user.balance.amount, user_old_balance)
        self.assertIn('You have exceeded your daily limit (10k) for ({})'.format(date.today()), response_data['error'])

    def testUploadAmountThatExceedsDailyLimitInOneTransaction(self):
        user_old_balance = self.user.balance.amount
        request_data = {"amount": 10001}
        self.amount_to_be_uploaded = request_data['amount']
        response = self.api_client.post(UPLOAD_MONEY_URL, data=request_data, **self.request_headers)
        response_data = response.json()
        self.assertEquals(response.status_code, 400)
        self.user = User.objects.get(email=self.user.email)
        self.assertEqual(self.user.balance.amount, user_old_balance)
        self.assertIn('Maximum amount to be uploaded 9999', response_data['error'])
    
    def testUploadMoneyWithUnAuthorizedUser(self):
        user_token = "invalid_token"
        unauthorized_headers = {'HTTP_AUTHORIZATION': '{} {}'.format(TOKEN_TYPE, user_token)}
        request_data = {"amount": 100}
        self.amount_to_be_uploaded = request_data['amount']
        response = self.api_client.post(UPLOAD_MONEY_URL, data=request_data, **unauthorized_headers)
        response_data = response.json()
        self.assertIn("Invalid token.", response_data['detail'])


    def testUploadMoney(self):
        user_old_balance = self.user.balance.amount
        request_data = {"amount": self.user.balance.amount + 100}
        self.amount_to_be_uploaded = request_data['amount']
        response = self.api_client.post(UPLOAD_MONEY_URL, data=request_data, **self.request_headers)
        response_data = response.json()
        self.assertEquals(response.status_code, 200)
        self.user = User.objects.get(email=self.user.email)
        self.assertEqual(Decimal(response_data['balance']), request_data['amount'] + user_old_balance)
        self.assertEqual(self.user.balance.amount, request_data['amount'] + user_old_balance)

 