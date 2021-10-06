from django.urls import path
from money.views.template_views import CurrencyExchange

urlpatterns = [
    path("currency/exchange", CurrencyExchange.as_view(), name="exhange_currency")
]
