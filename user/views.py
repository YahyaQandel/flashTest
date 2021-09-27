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
from money.models import MoneyUploaded
from user.serializer import LoginRequestSerializer, ResponseSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render
from django.shortcuts import redirect

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

class TemplateLogin(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'
    class_serializer = LoginRequestSerializer
    
    def get(self, request):
        if request.session.session_key:
            return redirect(to="/bank/connect")
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
            return redirect(to="/bank/connect")
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
    if "username" in request.data:
        login_args = {"username": request.data['username']}
        return True, login_args
    elif "email" in request.data:
        login_args = {"email": request.data['email']}
        return True, login_args
    else:
        return False, Response(
            data={"detail": "either provide your email or your username"},
            status=status.HTTP_401_UNAUTHORIZED)
    
