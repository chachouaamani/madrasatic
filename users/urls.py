from django.urls import path
from . import views
from .views import CompleteResetPassword, RequestPasswordResetEmail

from rest_framework import routers
from .views import ServiceViewSet , RoleViewSet,UsersViewSet

router = routers.DefaultRouter()
router.register('Service',ServiceViewSet)
router.register('Role',RoleViewSet)
router.register('Users',UsersViewSet)

urlpatterns = [
    path('signin/', views.signin_signup, name="signin&signup"),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    path('reset-password/', RequestPasswordResetEmail.as_view(), name="reset-password"),
    path('set-new-password/<uidb64>/<token>', CompleteResetPassword.as_view(), name='reset-user-password'),
    path('profile/', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('logout/', views.logout, name='logout'),


]

