from django.urls import path
from user.views import Login, Money

urlpatterns = [
    path("oauth/token", Login.as_view(), name="login"),
    path("user/money", Money.as_view(), name="upload"),
]
