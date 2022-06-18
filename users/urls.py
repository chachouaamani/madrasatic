from django.urls import path
from . import views
from .views import CompleteResetPassword, RequestPasswordResetEmail

from rest_framework import routers



from  .views import RegisterAPI
from .views import LoginAPI

from knox import views as knox_views

urlpatterns = [
    path('signin/', views.signin_signup, name="signin&signup"),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    path('reset-password/', RequestPasswordResetEmail.as_view(), name="reset-password"),
    path('set-new-password/<uidb64>/<token>', CompleteResetPassword.as_view(), name='reset-user-password'),
    path('profile/', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('logout/', views.logout, name='logout'),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

]

