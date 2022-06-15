from django.urls import path
from . import views


urlpatterns =[
    path('services/', views.service,name="services"),
    path('rapport/',views.rapport,name='rapport_service'),
    path('add_rapport/<int:id>',views.add_rapport,name='add_rapport'),
    path('view_rapport/<int:id>', views.view_rapport, name='view_rapport'),
    path('signal_content/<int:id>', views.signal_content, name='signal_data'),
    path('rapport_content/<int:id>', views.content_rapport, name='rapport_data'),
    path('notification_service/', views.notification, name="notification_service"),


]