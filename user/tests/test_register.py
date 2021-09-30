from django.test import TestCase
from rest_framework.test import APIClient
from user.models import User

# Create your tests here.
REGISTER_URL = '/user/register'


class TestRegister(TestCase):

    def testRegisterNewUser(self):
        data = {
            'email': "test@test.com",
            'password': "test_password",
            'username': "testUser"
        }
        api_client = APIClient()
        response = api_client.post(REGISTER_URL, data)
        self.assertEqual(response.status_code, 201)

    def testRegisterNewUserFailsWithoutEmail(self):
        data = {
            'password': "test_password",
            'username': "testUser"
        }
        api_client = APIClient()
        response = api_client.post(REGISTER_URL, data)
        self.assertEqual(response.status_code, 400)
        number_of_users = User.objects.filter(username=data['username']).count()
        response_data = response.json()
        self.assertEqual(response_data, {'email': ['This field is required.']})
        self.assertEqual(number_of_users, 0)

    def testRegisterNewUserFailsWithoutUsername(self):
        data = {
            'password': "test_password",
            'email': "test@test.com",
        }
        api_client = APIClient()
        response = api_client.post(REGISTER_URL, data)
        response_data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, {'username': ['This field is required.']})
        number_of_users = User.objects.filter(email=data['email']).count()
        self.assertEqual(number_of_users, 0)

    def testRegisterNewUserFailsWithoutPassword(self):
        data = {
            'email': "test@test.com",
            'username': "testUser"
        }
        api_client = APIClient()
        response = api_client.post(REGISTER_URL, data)
        response_data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, {'password': ['This field is required.']})
        number_of_users = User.objects.filter(username=data['username']).count()
        self.assertEqual(number_of_users, 0)