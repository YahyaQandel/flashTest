from rest_framework import serializers
from user.models import User


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class ResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'email',
            'phone'
        )
        model = User

    name = serializers.SerializerMethodField()

    def get_name(self, user):
        return '{} {}'.format(user.first_name, user.last_name)
