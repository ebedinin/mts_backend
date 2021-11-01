"""citsizi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from citsizi import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('citsizi/api/v2/certification/', include('certification_pc.urls')),
    path('citsizi/api/v2/', include('mts.api_v2.urls')),
    path('citsizi/api-auth/', include('rest_framework.urls')),
    path('citsizi/api-token-auth/', obtain_jwt_token),
    path('citsizi/api-token-refresh/', refresh_jwt_token),
    path('citsizi/api-token-verify/', verify_jwt_token),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
