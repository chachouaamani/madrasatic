from rest_framework import serializers


from users.models import Role , Service , Users
class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
