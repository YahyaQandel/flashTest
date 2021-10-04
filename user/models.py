from django.db import models
from django.contrib.auth.models import AbstractUser
from moneyed.classes import EGP
from rest_framework.authtoken.models import Token
from djmoney.models.fields import MoneyField
from rest_framework import status
from rest_framework.response import Response


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

    @staticmethod
    def serialize_params(request):
        login_args = None
        if "username" in request.data and "email" in request.data:
            login_args = {"username": request.data['username'], "email": request.data['email']}
            return True, login_args
        elif "username" in request.data:
            login_args = {"username": request.data['username']}
            return True, login_args
        elif "email" in request.data:
            login_args = {"email": request.data['email']}
            return True, login_args
        else:
            return False, Response(
                data={"detail": "either provide an email or a username"},
                status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def is_authorized(params, password):
        try:
            user = User.objects.get(**params)
            if not user.check_password(password):
                    return False, Response(
                        data={"detail": "The user credentials were incorrect."},
                        status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return False, Response(data={"detail": "The user credentials were incorrect."},
                            status=status.HTTP_401_UNAUTHORIZED)
        return True, user
