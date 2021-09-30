from django.test import TestCase
from rest_framework.test import APIClient
from user.factories import UserFactory
from rest_framework.authtoken.models import Token
from user.models import User
from user.tests.utils import get_request_authentication_headers

DELETE_URL = '/api/v1/user/delete'


class TestDelete(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.user = UserFactory(is_superuser=True)
        self.user_password = 'test_password'
        self.user.set_password(self.user_password)
        self.user.save()
        self.request_headers = get_request_authentication_headers(self.user)
        self.user_to_be_deleted = UserFactory()

    def testDeleteUser(self):
        request_url = "{}?username={}".format(DELETE_URL, self.user_to_be_deleted.username)
        response = self.api_client.delete(request_url, **self.request_headers)
        self.assertEqual(response.status_code, 200)
        self.assertRaises(User.DoesNotExist, User.objects.get, username=self.user_to_be_deleted.username)
    
    def testDeleteUserByUnauthorizedUser(self):
        unauthorized_user = UserFactory()
        request_url = "{}?username={}".format(DELETE_URL, self.user_to_be_deleted.username)
        request_headers = get_request_authentication_headers(unauthorized_user)
        response = self.api_client.delete(request_url, **request_headers)
        response_data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, {'error': ['only admin can delete users']})
        number_of_users = User.objects.filter(username=self.user_to_be_deleted.username).count()
        self.assertEqual(number_of_users, 1)
