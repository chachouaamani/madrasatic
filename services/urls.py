from django.urls import path
from . import views


urlpatterns =[
    path('services/', views.services,name="services"),
    path('edit_profile/', views.edit_profile,name="edit_profile"),
    path('sig/',views.sig,name='sig'),

]