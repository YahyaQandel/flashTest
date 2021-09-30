from django.urls import path
from money.views import Upload

urlpatterns = [
    path("upload", Upload.as_view(), name="upload"),
]
