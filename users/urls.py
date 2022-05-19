from django.urls import path
from . import views
from .views import CompleteResetPassword, RequestPasswordResetEmail

urlpatterns = [
    path('signin/', views.signin_signup, name="signin&signup"),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    path('reset-password/', RequestPasswordResetEmail.as_view(), name="reset-password"),
    path('set-new-password/<uidb64>/<token>', CompleteResetPassword.as_view(), name='reset-user-password'),


]

