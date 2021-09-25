from django.test import TestCase
from rest_framework.test import APIClient
from user.factories import UserFactory
from rest_framework.authtoken.models import Token
from user.models import User
from decimal import Decimal
from datetime import date,datetime,timedelta
from money.models import MoneyUploaded

TOKEN_TYPE = 'Bearer'
UPLOAD_MONEY_URL = "/user/money"


def get_request_authentication_headers(user):
    user_token = Token.objects.get(user_id=user.id)
    request_headers = {'HTTP_AUTHORIZATION': '{} {}'.format(TOKEN_TYPE, user_token)}
    return request_headers

# Create your tests here.


class TestUserMoney(TestCase):

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

    def testUploadMoneyExceedDailyLimit(self):
        request_data = {"amount": Decimal(9900)}
        self.amount_to_be_uploaded = request_data['amount']

        response = self.api_client.post(UPLOAD_MONEY_URL, data=request_data, **self.request_headers)
        response_data = response.json()
        self.assertEquals(response.status_code, 200)
        request_data = {"amount": Decimal(200)}
        response = self.api_client.post(UPLOAD_MONEY_URL, data=request_data, **self.request_headers)
        response_data = response.json()
        self.assertEquals(response.status_code, 400)
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


    # def tearDown(self) -> None:
    #     try:
    #         money_uploaded_today = MoneyUploaded.objects.filter(created_at__gte= datetime.now() - timedelta(days=1))
    #     except MoneyUploaded.DoesNotExist:
    #         pass
    #     if not money_uploaded_today:
    #         money_uploaded_now = MoneyUploaded(user=self.user, amount= self.amount_to_be_uploaded)
    #         money_uploaded_now.save()
    #     else:
    #         total_amount_uploaded_today = 0
    #         for one_time_upload in money_uploaded_today:
    #             total_amount_uploaded_today += one_time_upload.amount.amount
    #             print(one_time_upload.amount)
    #         print(total_amount_uploaded_today)

# test unaothorized user
# test user not exists and tries to upload money
# test upload exceeds daily limit
# test upload exceeds weekly limit