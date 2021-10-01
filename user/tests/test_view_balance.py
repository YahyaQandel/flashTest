from django.test import TestCase
from rest_framework.test import APIClient
from user.factories import UserFactory
from user.models import User
from user.tests.utils import get_request_authentication_headers

VIEW_BALANCE_URL = '/api/v1/user/balance'


class TestViewBalance(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.user = UserFactory(is_superuser=True)
        self.user_password = 'test_password'
        self.user.set_password(self.user_password)
        self.user.save()
        self.request_headers = get_request_authentication_headers(self.user)

    def testViewBalance(self):
        response = self.api_client.get(VIEW_BALANCE_URL, **self.request_headers)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.balance.amount, response_data['balance'])
    
    def testViewBalanceWithNotAuthonticatedUser(self):
        response = self.api_client.get(VIEW_BALANCE_URL)
        response_data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual({'detail': 'Authentication credentials were not provided.'},response_data)
    