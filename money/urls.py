from django.urls import path
from money.views import Upload

urlpatterns = [
    path("user/money", Upload.as_view(), name="upload"),
]
