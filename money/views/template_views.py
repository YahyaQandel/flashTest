from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.renderers import TemplateHTMLRenderer
from money.serializer import CurrencyExchangeSerializer

from django.shortcuts import redirect
from bank.views import get_logged_in_user
import requests
from django.conf import settings

DAILY_LIMIT = 10000
WEEKLY_LIMIT = 50000

class CurrencyExchange(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'currency_exchange.html'
    class_serializer = CurrencyExchangeSerializer
    LOGIN_PAGE_URL = "/login"

    def get(self, request):
        if request.session.session_key:
            try:
                user = get_logged_in_user(request)
            except Session.DoesNotExist:
                return redirect(to=self.LOGIN_PAGE_URL)
            default_base_cur = 'EUR'
            rates = self.get_currenceis_rate(default_base_cur)
            currencies = self.get_currencies_from_rate_api(rates)
            new_balance_in_default_rate = self.get_user_balance_in_currency(user,default_base_cur)
            response_data = {'rates': rates,
                            'balance': new_balance_in_default_rate,
                            'currencies': currencies,
                            'base_curr': default_base_cur}

            return Response(response_data)
        else:
            return redirect(to="/login")

    def post(self, request):
        if request.session.session_key:
            user = get_logged_in_user(request)
        else:
            return redirect(to=self.LOGIN_PAGE_URL)
        serializer = CurrencyExchangeSerializer(data=request.data)
        is_valid_params = serializer.is_valid(raise_exception=False)
        if not is_valid_params:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        base_currency = request.data['currency']
        rates = self.get_currenceis_rate(base_currency)
        user_currency = str(user.balance.currency)
        new_balance_in_default_rate = round(float(user.balance.amount ) * float(rates[user_currency]), 2)
        currencies = self.get_currencies_from_rate_api(rates)
        return Response({'balance': new_balance_in_default_rate,'rates': rates,'currencies': currencies, 'base_curr': base_currency})

    def get_currenceis_rate(self, base_currency):
        ploads = {'access_key': settings.CURRENCIES_KEY}
        api_url = "{}".format(settings.CURRENCIES_API)
        r = requests.get(api_url, params=ploads)
        currencies_rates_response = r.json()
        rates = currencies_rates_response['rates']
        response_rates = {}
        exchange_rate = 1 * rates[base_currency]
        for key, value in rates.items():
            response_rates[key] = round(rates[key] / exchange_rate, 5)
        return response_rates

    def get_user_balance_in_currency(self, user, currency):
        rates = self.get_currenceis_rate(currency)
        user_currency = str(user.balance.currency)
        return round(float(user.balance.amount ) * float(rates[user_currency]), 2)


    def get_currencies_from_rate_api(self, rates):
        currencies = []
        for currency , _ in rates.items():
            currencies.append(currency)
        return currencies