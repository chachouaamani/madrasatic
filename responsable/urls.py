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
path('category_table/', views.category_table, name="category_service"),
path('service_table/', views.service_table, name="service_table"),
path('add_service/', views.add_service, name="add_service"),
path('add_category/', views.add_category, name="add_category"),
path('statistique/', views.test, name="statistic"),
path('content_archive/<int:id>', views.content_signal_archivé, name="content_archive"),
path('archive/', views.archive, name="archive"),
path('notification/', views.notification, name="notification"),

]