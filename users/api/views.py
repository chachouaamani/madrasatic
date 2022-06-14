from rest_framework import status
from rest_framework.response import  Response
from rest_framework.decorators import api_view

from users.models import Service
from users.models import Role
from users.models import Users

from users.api.serializers import ServicesSerializer,RoleSerializer,UsersSerializer


@api_view (['GET','POST'])
def api_role_views(request,slug4):
    try:
        role = Role.objects.get(slug=slug4)
    except Role.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=="GET":
        serializer=RoleSerializer(role)
        return Response(serializer.data)

@api_view (['GET','POST'])
def api_service_views(request,slug5):
    try:
        service = Service.objects.get(slug=slug5)
    except Service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=="GET":
        serializer=ServicesSerializer(service)
        return Response(serializer.data)

@api_view (['GET','POST'])
def api_users_views(request,slug6):
    try:
        user= Users.objects.get(slug=slug6)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=="GET":
        serializer=UsersSerializer(user)
        return Response(serializer.data)
