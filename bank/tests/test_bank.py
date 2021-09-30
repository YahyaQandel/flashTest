from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from bank.factories import BankFactory
TOKEN_TYPE = 'Bearer'
BANK_DISCONNECT = "/bank/disconnect"
BANK_CONNECT = "/bank/api/connect"

from user.tests.utils import get_request_authentication_headers

# Create your tests here.


class TetsBankOperations(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.bank = BankFactory()
        self.request_headers = get_request_authentication_headers(self.bank.user)
        self.amount_to_be_uploaded = 0

    def testDisconnectBankAccount(self):
        account_number = self.bank.account_number
        request_url = "{}?account_number={}".format(BANK_DISCONNECT, account_number)
        response = self.api_client.delete(request_url, **self.request_headers)
        response_data = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_data, {})

    def testConnectBankAccount(self):
        request_data = {"bank_name": "CIB",
                        "branch_number": "123",
                        "account_number": "123123123",
                        "account_holder_name": "yahya"}

        response = self.api_client.post(BANK_CONNECT, data=request_data, **self.request_headers)
        self.assertEquals(response.status_code, 201)
