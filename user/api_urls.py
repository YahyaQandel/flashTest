from django.urls import path
from user.views import Register, Remove, Balance

urlpatterns = [
    path("register", Register.as_view(), name="register"),
    path("delete", Remove.as_view(), name="delete"),
    path("balance", Balance.as_view(), name="balance")
]
