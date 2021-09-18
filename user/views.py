from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializer import LoginRequestSerializer, ResponseSerializer


class UserApi(APIView):
    class_serializer = LoginRequestSerializer

    def post(self, request, format=None):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user_password = request.data['password']
            user = User.objects.get(email=request.data['email'])
            if not user.check_password(user_password):
                return Response(
                    data={"detail": "The user credentials were incorrect."},
                    status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response(data={"detail": "The user credentials were incorrect."},
                            status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data=ResponseSerializer(user).data, status=status.HTTP_200_OK)
