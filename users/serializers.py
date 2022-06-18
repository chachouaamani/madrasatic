from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()






# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','first_name','last_name')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','first_name','last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}



    def create(self, validated_data):
        user = User.objects.create_user(
            self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            password=self.validated_data['password']
        )

        return user




