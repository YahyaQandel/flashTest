from factory import django, Faker, post_generation
from user.models import User
from rest_framework.authtoken.models import Token


class UserFactory(django.DjangoModelFactory):
    email = Faker("email")
    username = Faker("name")

    @post_generation
    def create_token(self, create: bool, extracted, **kwargs):
        Token.objects.get_or_create(user=self)

    class Meta:
        model = User
        django_get_or_create = ["username"]
