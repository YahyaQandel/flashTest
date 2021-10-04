from django.urls import path
from user.views.template_views import TemplateLogin, UnAuthorized
from user.views.api_views import Login

urlpatterns = [
    path("oauth/token", Login.as_view(), name="api_login"),
    path("login", TemplateLogin.as_view(), name="template_login"),
    path("unauthorized", UnAuthorized.as_view(), name="access_denied"),
]
