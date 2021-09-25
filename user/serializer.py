from rest_framework import serializers
from user.models import User


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    password = serializers.CharField()
    username = serializers.CharField(required=False)


class ResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'balance'
        )
        model = User


class MoneyRequestSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=1.0)
