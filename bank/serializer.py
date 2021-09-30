from rest_framework import serializers
from user.models import User


class ConnectSerializer(serializers.Serializer):
    bank_name = serializers.CharField(required=True)
    branch_number = serializers.CharField(required=True)
    account_number = serializers.CharField(required=True)
    account_holder_name = serializers.CharField(required=True)
    name_ref = serializers.CharField(required=False)


class DisconnectSerializer(serializers.Serializer):
    account_number = serializers.CharField(required=True)
