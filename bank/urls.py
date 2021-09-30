from django.urls import path
from bank.views import Connect, Connected, Disconnect, ApiConnect
urlpatterns = [
    path("connect", Connect.as_view(), name="connect"),
    path("api/connect", ApiConnect.as_view(), name="api_connect"),
    path("connected", Connected.as_view(), name="connected"),
    path("disconnect", Disconnect.as_view(), name="disconnect")
]
