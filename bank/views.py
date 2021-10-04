from moneyed.classes import EGP
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from bank.serializer import ConnectSerializer

from bank.models import Bank
from user.models import User
class Connect(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'connect_to_bank.html'
    class_serializer = ConnectSerializer

    def get(self, request):
        if request.session.session_key:
            return Response()
        else:
            return redirect(to="/login")

    def post(self, request):
        if request.session.session_key:
            print("xxxxxxxxx",request.session.session_key)
            user = get_logged_in_user(request)
        elif request.user:
            user = request.user
        else:
            return redirect(to="/login")
        serializer = ConnectSerializer(data=request.data)
        is_valid_params = serializer.is_valid(raise_exception=False)
        if not is_valid_params:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        bank_details = get_data_from_request_params(request)
        bank = Bank(user=user, **bank_details)
        bank.save()
        if request.session.session_key:
            return redirect(to="/bank/connected")
        return Response({}, status=status.HTTP_201_CREATED)


class ApiConnect(APIView):
    class_serializer = ConnectSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def post(self, request):
        serializer = ConnectSerializer(data=request.data)
        is_valid_params = serializer.is_valid(raise_exception=False)
        if not is_valid_params:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        bank_details = get_data_from_request_params(request)
        user = request.user
        bank = Bank(user=user, **bank_details)
        bank.save()
        return Response({}, status=status.HTTP_201_CREATED)

def get_data_from_request_params(request):
    request_data = {}
    for key,value in request.data.items():
        request_data[key] = value
    return request_data


class Connected(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'connected_to_bank.html'
    class_serializer = ConnectSerializer

    def get(self, request):
        bank = None
        try:
            user = get_logged_in_user(request)
            bank = Bank.objects.filter(user=user).last()
            if not bank:
                return redirect(to="/bank/connect")
        except Bank.DoesNotExist:
            return redirect(to="/bank/connect")
        
        return Response({'bank_name': bank.bank_name, 'account_number': bank.account_number})


def get_logged_in_user(request):
    session = Session.objects.get(session_key=request.session.session_key)
    session_data = session.get_decoded()
    uid = session_data['user']
    user = User.objects.get(id=uid)
    return user

def is_user_connected_to_bank(user):
    try:
        connected_to_bank = Bank.objects.filter(user=user).last()
        if not connected_to_bank:
            return False
    except Bank.DoesNotExist:
        return False
    return connected_to_bank


class Disconnect(APIView):

    permission_classes = (
        IsAuthenticated,
    )
    def delete(self, request):
        if "account_number" not in request.GET:
            return Response(data={"account_number": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        bank = None
        try:
            account_number = request.GET['account_number']
            bank = Bank.objects.get(user=request.user, account_number=account_number)
            if not bank:
                print(bank)
                return Response(data={'error': 'account id not found'}, status=status.HTTP_404_NOT_FOUND)
        except Bank.DoesNotExist:
            return Response(data={'error': 'account id not found'}, status=status.HTTP_404_NOT_FOUND)
        bank.delete()
        return Response(data={}, status=status.HTTP_200_OK)