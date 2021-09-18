from django.urls import path
from user.views import UserApi

urlpatterns = [
    path("v2/oauth/token", UserApi.as_view(), name="login"),
]
