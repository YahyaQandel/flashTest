from factory import django, Faker, post_generation
import factory
from user.factories import UserFactory
from bank.models import Bank,BANKS
import random

class BankFactory(django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    bank_name = random.choice(BANKS.choices)[0]
    branch_number = "325"
    account_number = "C16516576507"
    account_holder_name = "JOHN DOE"

    class Meta:
        model = Bank
