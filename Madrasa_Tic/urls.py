"""Madrasa_Tic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home_user, name='home_user')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home_user')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


from django.urls import path, include
from rest_framework import routers
from users.urls import router as users_router
from home_user.urls import router as home_user_router
router = routers.DefaultRouter()
router.registry.extend(users_router.registry)
router.registry.extend(home_user_router.registry)


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('users/', include('users.urls')),
    path('', include('welcome.urls')),
    path('home_user/', include('home_user.urls')),
    path('responsable/', include('responsable.urls')),
    path('services/', include('services.urls')),
    path('amani/',include(router.urls)),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



