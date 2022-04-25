from django.urls import path
from . import views

urlpatterns = [

path('', views.declaration, name="declaration"),
path('manage/', views.manage, name="manage"),
]