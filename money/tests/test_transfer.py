from django.test import TestCase
from rest_framework.test import APIClient
from user.factories import UserFactory
from rest_framework.authtoken.models import Token
from user.models import User
from decimal import Decimal
from datetime import date, datetime, timedelta
from money.models import MoneyUploaded, Transaction
import moneyed
from user.tests.utils import get_request_authentication_headers
from bank.factories import BankFactory
from django.test import TestCase
from rest_framework.test import APIClient
from user.factories import UserFactory
from rest_framework.authtoken.models import Token
from user.models import User
from decimal import Decimal
from datetime import date, datetime, timedelta
from money.models import MoneyUploaded
import moneyed
from user.tests.utils import get_request_authentication_headers
from bank.factories import BankFactory
from bank.models import Bank

TOKEN_TYPE = 'Bearer'
TRANSFER_MONEY_URL = "/api/v1/money/transfer"


class TestTransfer(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.bank = BankFactory()
        self.user = self.bank.user
        self.bank.user.balance = moneyed.Money(amount=1000, currency='EGP')
        self.bank.user.save()
        self.request_headers = get_request_authentication_headers(self.user)
        self.amount_to_be_transferred= 0
        self.recipient_user = UserFactory()

    # test user authorized to transfer

    def testInsufficientBalanceFails(self):
        recipient_user_balance_before_transfer_operation = self.recipient_user.balance.amount
        sender_user_balance_before_transfer_operation = self.user.balance.amount
        request_data = {"amount": Decimal(2000), 'username': self.recipient_user.username}
        response = self.api_client.post(TRANSFER_MONEY_URL, data=request_data, **self.request_headers)
        response_data = response.json()
        self.assertIn('Insufficient balance', response_data['error'])
        self.assert_failure_400_and_sender_and_recipient_balances_not_changed(response,
                                                        sender_user_balance_before_transfer_operation,
                                                        recipient_user_balance_before_transfer_operation)    

    def testTransferToInvalidRecipientUsername(self):
        sender_user_balance_before_transfer_operation = self.user.balance.amount
        request_data = {"amount": Decimal(100), 'username': "invalidUserName"}
        response = self.api_client.post(TRANSFER_MONEY_URL, data=request_data, **self.request_headers)
        response_data = response.json()
        self.assertIn('user not found', response_data['error'])
        self.assertEquals(response.status_code, 404)
        self.current_sender = User.objects.get(email=self.user.email)
        self.assertEqual(self.current_sender.balance.amount, sender_user_balance_before_transfer_operation)

    def testTransferInvalidAmount(self):
        sender_user_balance_before_transfer_operation = self.user.balance.amount
        recipient_user_balance_before_transfer_operation = self.recipient_user.balance.amount
        request_data = {"amount": "f", 'username': self.recipient_user.username}
        response = self.api_client.post(TRANSFER_MONEY_URL, data=request_data, **self.request_headers)
        response_data = response.json()
        self.assertIn('A valid number is required.', response_data['amount'])
        self.assert_failure_400_and_sender_and_recipient_balances_not_changed(response,
                                                        sender_user_balance_before_transfer_operation,
                                                        recipient_user_balance_before_transfer_operation)

    def testTransferMoneyExceedDailyLimit(self):
        self.bank.user.balance = moneyed.Money(amount=15000, currency='EGP')
        self.bank.user.save()
        request_data = {"amount": Decimal(9900), "username": self.recipient_user.username}
        response = self.api_client.post(TRANSFER_MONEY_URL, data=request_data, **self.request_headers)
        self.assertEquals(response.status_code, 200)
        sender_user_balance_before_transfer_operation = User.objects.filter(username=self.user.username).last().balance.amount
        recipient_user_balance_before_transfer_operation = User.objects.filter(username=self.recipient_user.username).last().balance.amount
        request_data = {"amount": Decimal(101), "username": self.recipient_user.username}
        response = self.api_client.post(TRANSFER_MONEY_URL, data=request_data, **self.request_headers)
        response_data = response.json()
        self.assertIn('You have exceeded your daily transfer limit (10k) for ({})'.format(date.today()), response_data['error'])
        self.assert_failure_400_and_sender_and_recipient_balances_not_changed(response,
                                                        sender_user_balance_before_transfer_operation,
                                                        recipient_user_balance_before_transfer_operation)
    
    def testTransferAmountThatExceedsDailyLimitInOneTransaction(self):
        self.bank.user.balance = moneyed.Money(amount=15000, currency='EGP')
        self.bank.user.save()
        sender_user_balance_before_transfer_operation = self.user.balance.amount
        recipient_user_balance_before_transfer_operation = self.recipient_user.balance.amount
        request_data = {"amount": Decimal(10001), "username": self.recipient_user.username}
        response = self.api_client.post(TRANSFER_MONEY_URL, data=request_data, **self.request_headers)
        response_data = response.json()
        self.assertIn('Maximum amount to be transferred 9999', response_data['error'])
        self.assert_failure_400_and_sender_and_recipient_balances_not_changed(response,
                                                        sender_user_balance_before_transfer_operation,
                                                        recipient_user_balance_before_transfer_operation)

    def testTransferMoneyExceedingWeeklyLimit(self):
        self.bank.user.balance = moneyed.Money(amount=100000, currency='EGP')
        self.bank.user.save()
        request_data = {"amount": Decimal(7000), "username": self.recipient_user.username}
        self.amount_to_be_transferred = request_data['amount']
        today = datetime.today()
        daily_amount = 7500
        for i in range(1, 10):
            day_before = today - timedelta(days=i)
            day_before_transferred_money_obj = Transaction(sender=self.user, amount=daily_amount + i*10, recipient=self.recipient_user)
            day_before_transferred_money_obj.save()
            day_before_transferred_money_obj.created_at = day_before.date()
            day_before_transferred_money_obj.save()
            self.user.balance = self.user.balance - moneyed.Money(amount=daily_amount, currency='EGP')
            self.user.save()
            self.recipient_user.balance = self.recipient_user.balance + moneyed.Money(amount=daily_amount, currency='EGP')
            self.recipient_user.save()

        sender_user_balance_before_transfer_operation = self.user.balance.amount
        recipient_user_balance_before_transfer_operation = self.recipient_user.balance.amount
        response = self.api_client.post(TRANSFER_MONEY_URL, data=request_data, **self.request_headers)
        response_data = response.json()
        self.assertIn('You have exceeded your weekly transfer limit (50k)'.format(date.today()), response_data['error'])
        self.assert_failure_400_and_sender_and_recipient_balances_not_changed(response,
                                                        sender_user_balance_before_transfer_operation,
                                                        recipient_user_balance_before_transfer_operation)

    def testTransferMoneyNotExceedingWeeklyLimit(self):
        self.bank.user.balance = moneyed.Money(amount=100000, currency='EGP')
        self.bank.user.save()
        request_data = {"amount": Decimal(100), "username": self.recipient_user.username}
        self.amount_to_be_transferred = request_data['amount']
        today = datetime.today()
        daily_amount = 2000
        for i in range(1, 10):
            day_before = today - timedelta(days=i)
            day_before_transferred_money_obj = Transaction(sender=self.user, amount=daily_amount + i*10, recipient=self.recipient_user)
            day_before_transferred_money_obj.save()
            day_before_transferred_money_obj.created_at = day_before.date()
            day_before_transferred_money_obj.save()
            self.user.balance = self.user.balance - moneyed.Money(amount=daily_amount, currency='EGP')
            self.user.save()
            self.recipient_user.balance = self.recipient_user.balance + moneyed.Money(amount=daily_amount, currency='EGP')
            self.recipient_user.save()

        sender_user_balance_before_transfer_operation = self.user.balance.amount
        recipient_user_balance_before_transfer_operation = self.recipient_user.balance.amount
        response = self.api_client.post(TRANSFER_MONEY_URL, data=request_data, **self.request_headers)
        self.assertEquals(response.status_code, 200)
        self.current_sender = User.objects.get(email=self.user.email)
        self.assertEqual(self.current_sender.balance.amount, sender_user_balance_before_transfer_operation - self.amount_to_be_transferred)
        self.current_recipient = User.objects.get(email=self.recipient_user.email)
        self.assertEqual(self.current_recipient.balance.amount, recipient_user_balance_before_transfer_operation + self.amount_to_be_transferred)

    def testTransferMoneySucceeds(self):
        self.bank.user.balance = moneyed.Money(amount=10000, currency='EGP')
        self.bank.user.save()
        sender_user_balance_before_transfer_operation = self.user.balance.amount
        recipient_user_balance_before_transfer_operation = self.recipient_user.balance.amount
        request_data = {"amount": Decimal(5000), "username": self.recipient_user.username}
        self.amount_to_be_transferred = request_data['amount']
        response = self.api_client.post(TRANSFER_MONEY_URL, data=request_data, **self.request_headers)
        self.assert_success_200_and_sender_and_recipient_balances_changed(response,
                                                        sender_user_balance_before_transfer_operation,
                                                        recipient_user_balance_before_transfer_operation)

    def testTransferMoneyByProvidingRecipientEmailSucceeds(self):
        self.bank.user.balance = moneyed.Money(amount=10000, currency='EGP')
        self.bank.user.save()
        sender_user_balance_before_transfer_operation = self.user.balance.amount
        recipient_user_balance_before_transfer_operation = self.recipient_user.balance.amount
        request_data = {"amount": Decimal(5000), "email": self.recipient_user.email}
        self.amount_to_be_transferred = request_data['amount']
        response = self.api_client.post(TRANSFER_MONEY_URL, data=request_data, **self.request_headers)
        self.assert_success_200_and_sender_and_recipient_balances_changed(response,
                                                        sender_user_balance_before_transfer_operation,
                                                        recipient_user_balance_before_transfer_operation)

    def assert_failure_400_and_sender_and_recipient_balances_not_changed(self,response,
                                            sender_user_balance_before_transfer_operation,
                                            recipient_user_balance_before_transfer_operation):
            self.assertEquals(response.status_code, 400)
            self.current_sender=User.objects.get(email=self.user.email)
            self.assertEqual(self.current_sender.balance.amount, sender_user_balance_before_transfer_operation)
            self.current_recipient=User.objects.get(email=self.recipient_user.email)
            self.assertEqual(self.current_recipient.balance.amount, recipient_user_balance_before_transfer_operation)


    def assert_success_200_and_sender_and_recipient_balances_changed(self,response,
                                            sender_user_balance_before_transfer_operation,
                                            recipient_user_balance_before_transfer_operation):
        self.assertEquals(response.status_code, 200)
        self.current_sender = User.objects.get(email=self.user.email)
        self.current_recipient = User.objects.get(email=self.recipient_user.email)
        self.assertEqual(self.current_sender.balance.amount, sender_user_balance_before_transfer_operation - self.amount_to_be_transferred)
        self.assertEqual(self.current_recipient.balance.amount, recipient_user_balance_before_transfer_operation + self.amount_to_be_transferred)