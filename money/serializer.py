from rest_framework import serializers
from user.models import User


class MoneyRequestSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=1.0)
