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
        is_valid_params, response = validate_login_request_params(request)
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
        is_valid_params, response = validate_login_request_params(request)
        if not is_valid_params:
            return response
        params = response
        is_valid_login_creds, response = validate_user_login(params=params, password=request.data['password'])
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



class TemplateLogin(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'
    class_serializer = LoginRequestSerializer
    
    def get(self, request):
        # if request.session.session_key:
        #     return redirect(to="/bank/connect")
        return Response()

    def post(self, request, format=None):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_valid_params, response = validate_login_request_params(request)
        if not is_valid_params:
            return response
        params = response
        is_valid_login_creds, response = validate_user_login(params=params, password=request.data['password'])
        if is_valid_login_creds:
            user = response
            request.session.set_test_cookie()
            request.session['user'] = user.id
            if not is_user_connected_to_bank(user):
                return redirect(to="/bank/connect")
            else:
                return redirect(to="/bank/connected")
        else:
            return redirect(to="/unauthorized")


class UnAuthorized(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'unauthorized.html'
    class_serializer = LoginRequestSerializer
    
    def get(self, request):
        return Response()


def validate_user_login(params, password):
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


def validate_login_request_params(request):
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
            data={"detail": "either provide your email or your username"},
            status=status.HTTP_401_UNAUTHORIZED)
    

class Balance(APIView):
    permission_classes = (
        IsAuthenticated,
    )

    def get(self, request):
        return Response({"balance": request.user.balance.amount}, status=status.HTTP_200_OK)