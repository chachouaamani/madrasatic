import os
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

def filepath(request,filename):
    old_filename=filename
    timeNow=datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename="%s%s" %(timeNow,old_filename)
    return os.path.join('uploads/',filename)

class Users(AbstractUser):
    role = models.CharField(max_length=50, null=False, default="utilisateur")
    image = models.ImageField(null=False, blank=True, upload_to=filepath)

    def __str__(self):
        return self.username


class Service(models.Model):
    name=models.CharField(max_length=50,null=False,default="None",unique=True)
    description=models.TextField(max_length=100,null=False,default="None")

    def __str__(self):
        return self.name






