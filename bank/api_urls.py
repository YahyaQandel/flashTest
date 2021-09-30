from django.urls import path
from bank.views import Connect, Connected, Disconnect, ApiConnect
urlpatterns = [
    path("connect", ApiConnect.as_view(), name="api_connect"),
    path("disconnect", Disconnect.as_view(), name="disconnect")
]
