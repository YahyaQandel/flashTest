from rest_framework import serializers
from user.models import User


class MoneyRequestSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=1.0)

class TransferRequestSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=1.0)
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)


class CurrencyExchangeSerializer(serializers.Serializer):
    currency = serializers.CharField()