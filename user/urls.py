from django.urls import path
from user.views import Login, TemplateLogin,UnAuthorized

urlpatterns = [
    path("oauth/token", Login.as_view(), name="api_login"),
    path("login", TemplateLogin.as_view(), name="template_login"),
    path("unauthorized", UnAuthorized.as_view(), name="access_denied")
]
