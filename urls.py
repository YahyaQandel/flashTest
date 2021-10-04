from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from user.views.template_views import TemplateLogin, UnAuthorized
from user.views.api_views import Login

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('user/', include('user.urls')),
    path('bank/', include('bank.urls')), 
    path('money/', include('money.urls.template_urls')), 
    path('api/v1/money/', include('money.urls.api_urls')), 
    path('api/v1/bank/', include('bank.api_urls')), 
    path('api/v1/user/', include('user.urls.api_urls')), 
    path('', include('user.urls.template_urls')), 
    path("", TemplateLogin.as_view(), name="template_login"),
] 