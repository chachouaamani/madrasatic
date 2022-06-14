from django.urls import path
from users.api.views import  api_role_views,api_service_views,api_users_views

app_name='users'

urlpatterns=[
    path('<slug4>/', api_role_views,name="detail"),
    path('<slug5>/', api_service_views,name="detail"),
    path('<slug6>/', api_users_views,name="detail")
]
