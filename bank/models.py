from django.db import models
from user.models import User
# Create your models here.
from model_utils.models import SoftDeletableModel
from django.utils.translation import gettext_lazy as _

class BANKS(models.TextChoices):
    CIB = 'CIB', _('CIB')
    HSBC = 'HSBC', _('HSBC')
    QNB = 'QNB', _('QNB')

class Bank(SoftDeletableModel):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=9, choices=BANKS.choices,
                  default=BANKS.CIB)
    branch_number = models.CharField('Branch_name', max_length=100,)
    account_number = models.CharField('Account_number', max_length=100, unique=True,)
    account_holder_name = models.CharField('Account_holder_name', max_length=100,)
    name_ref = models.CharField('Bank_name', max_length=100,)