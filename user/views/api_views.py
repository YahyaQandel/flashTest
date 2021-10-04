from decimal import Decimal
import re
from moneyed.classes import EGP
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseRedirect

from datetime import date, datetime, timedelta

from user.models import User
from user.serializer import LoginRequestSerializer, ResponseSerializer, UserSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render
from django.shortcuts import redirect
from bank.views import is_user_connected_to_bank

from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth.decorators import user_passes_test

from user.serializer import RegisterUserSerializer, LoginRequestSerializer


class Register(APIView):

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_valid_params, response = User.serialize_params(request)
        if not is_valid_params:
            return response
        user_params = response
        user = User(**user_params)
        user.set_password(request.data['password'])
        user.save()
        return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED)

class Login(APIView):

    class_serializer = LoginRequestSerializer

    def post(self, request, format=None):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_valid_params, response = User.serialize_params(request)
        if not is_valid_params:
            return response
        params = response
        is_valid_login_creds, response = User.is_authorized(params=params, password=request.data['password'])
        if is_valid_login_creds:
            user = response
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data=ResponseSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return response

class Remove(APIView):

    def delete(self, request):
        if not request.user or not request.user.is_superuser:
            return Response(data={"error": ["only admin can delete users"]}, status=status.HTTP_400_BAD_REQUEST)

        if "username" not in request.GET:
            return Response(data={"username": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        user = None
        try:
            username = request.GET['username']
            user = User.objects.get(username=username)
            if not user:
                return Response(data={'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response(data={'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(data={}, status=status.HTTP_200_OK)

class Balance(APIView):
    permission_classes = (
        IsAuthenticated,
    )

    def get(self, request):
        return Response({"balance": request.user.balance.amount}, status=status.HTTP_200_OK)
