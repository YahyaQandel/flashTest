from factory import django, Faker, post_generation
import factory
from user.models import User
from rest_framework.authtoken.models import Token
import random


class UserFactory(django.DjangoModelFactory):
    email = Faker("email")
    username = Faker("first_name")
    balance = factory.Faker('pyint', min_value=0, max_value=100)
    is_staff = False
    is_superuser = False

    class Params: 
        # declare a trait that adds relevant parameters for admin users
        flag_is_superuser = factory.Trait(
            is_superuser=True,
            is_staff=True,
        )

    @post_generation
    def create_token(self, create: bool, extracted, **kwargs):
        Token.objects.get_or_create(user=self)

    class Meta:
        model = User
        django_get_or_create = ["username"]
