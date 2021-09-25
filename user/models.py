from django.db import models
from django.contrib.auth.models import AbstractUser
from moneyed.classes import EGP
from rest_framework.authtoken.models import Token
from djmoney.models.fields import MoneyField


class User(AbstractUser):
    username = models.CharField('Username', max_length=100, unique=True,)
    email = models.EmailField('Email', max_length=100, unique=True,)
    balance = MoneyField(max_digits=10, decimal_places=2, null=True, default_currency='EGP', default=0
                        )    

    @property
    def token(self):
        token, _ = Token.objects.get_or_create(user=self)
        return token

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
