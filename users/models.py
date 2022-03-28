from django.db import models


# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=20, null=False, default="anything" )
    name = models.CharField(max_length=50, null= False, default="anything")
    surname = models.CharField(max_length=50, null=False, default="anything")
    email = models.EmailField(max_length=50, null=False, default="anything")
    password = models.CharField(max_length=20, null=False, default="anything")
    is_email_verified = models.BooleanField(default=False)


