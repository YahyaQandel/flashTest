from django.urls import path
from user.views import Register, Remove

urlpatterns = [
    path("register", Register.as_view(), name="register"),
    path("delete", Remove.as_view(), name="delete")
]
