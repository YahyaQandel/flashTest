from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from user.views import TemplateLogin, UnAuthorized
from user.views import Login, TemplateLogin, UnAuthorized

urlpatterns = [
    path('admin/', admin.site.urls),
    path("oauth/token", Login.as_view(), name="api_login"),
    path("login", TemplateLogin.as_view(), name="template_login"),
    path("unauthorized", UnAuthorized.as_view(), name="access_denied"),
    path('user/', include('user.urls')),
    path('bank/', include('bank.urls')), 
    path('money/', include('money.urls')), 
    path('api/v1/money/', include('money.api_urls')), 
    path('api/v1/bank/', include('bank.api_urls')), 
    path('api/v1/user/', include('user.api_urls')), 
    path("", TemplateLogin.as_view(), name="template_login"),
] 