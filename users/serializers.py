

from rest_framework import serializers
from .models import Service , Role , Users

class ServiceSerializer (serializers.ModelSerializer):
    class Meta :
        model = Service
        fields= '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
