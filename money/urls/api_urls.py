from django.urls import path
from money.views.api_views import Upload, Transfer

urlpatterns = [
    path("upload", Upload.as_view(), name="upload"),
    path("transfer", Transfer.as_view(), name="transfer")
]
