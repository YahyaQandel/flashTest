from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from user.views import TemplateLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')), 
    path('', include('money.urls')), 
    path('bank/', include('bank.urls')), 
    path("", TemplateLogin.as_view(), name="template_login"),
] 