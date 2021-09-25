from factory import django, Faker, post_generation
import factory
from user.models import User
from rest_framework.authtoken.models import Token
import random


class UserFactory(django.DjangoModelFactory):
    email = Faker("email")
    username = Faker("name")
    balance = factory.Faker('pyint', min_value=0, max_value=100)

    @post_generation
    def create_token(self, create: bool, extracted, **kwargs):
        Token.objects.get_or_create(user=self)

    class Meta:
        model = User
        django_get_or_create = ["username"]
