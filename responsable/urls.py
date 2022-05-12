from django.urls import path
from . import views

urlpatterns = [

path('manage/', views.manage, name="manage"),
path('content/<int:id>', views.content, name="content"),
]