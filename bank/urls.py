from django.urls import path
from bank.views import Connect, Connected
urlpatterns = [
    path("connect", Connect.as_view(), name="connect"),
    path("connected", Connected.as_view(), name="connected"),
]
