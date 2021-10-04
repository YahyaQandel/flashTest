from moneyed.classes import EGP
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializer import LoginRequestSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render
from django.shortcuts import redirect
from bank.views import is_user_connected_to_bank

from django.contrib.auth.decorators import user_passes_test
from user.serializer import  LoginRequestSerializer

class TemplateLogin(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'
    class_serializer = LoginRequestSerializer
    
    def get(self, request):
        return Response()

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

