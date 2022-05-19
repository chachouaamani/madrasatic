from django.urls import path
from . import views

urlpatterns = [

path('manage/', views.manage, name="manage"),
path('content/<int:id>', views.content_signal, name="content"),
path('content_annonce/<int:id>', views.content_annonce, name="content_annonce"),
path('content_rapport/<int:id>', views.content_rapport, name="content_rapport"),
path('rapport/', views.rapport, name="rapport"),
path('service_manage/<int:id>', views.service_manage, name="service_manage"),
path('category_manage/<int:id>', views.category_manage, name="category_manage"),
path('annonce/', views.annonce, name="annonce"),
path('category_service/', views.category_table, name="category_service"),
path('add_service/', views.add_service, name="add_service"),
path('add_category/', views.add_category, name="add_category"),

]