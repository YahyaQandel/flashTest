from django.db import models
from django.contrib.auth.models import AbstractUser
from model_utils.models import SoftDeletableModel, TimeStampedModel
from moneyed.classes import EGP
from rest_framework.authtoken.models import Token
from djmoney.models.fields import MoneyField
from user.models import User

class MoneyUploaded(SoftDeletableModel):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=10, decimal_places=2, null=True, default_currency='EGP', default=0
                        )
    created_at = models.DateField(auto_now_add=True)
