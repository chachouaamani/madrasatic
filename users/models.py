import os
import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)





class Service(models.Model):
    name = models.CharField(max_length=50, null=False, default="None", unique=True)
    description = models.TextField(max_length=100, null=False, default="None")

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50, null=False, default="utilisateur",unique=True)
    service = models.ForeignKey(Service, on_delete=models.RESTRICT, default=1)

    def __str__(self):
        return self.name

class Users(AbstractUser):
    role =models.ForeignKey(Role, on_delete=models.RESTRICT, default=1)
    image = models.ImageField(null=False, blank=True, upload_to=filepath)

    @property
    def is_admin(self):
        if self.role.name == "club" or self.role.name == "administration":
            return True

    @property
    def is_responsable(self):
        if self.role.name == "responsable" :
            return True

    @property
    def is_service(self):
        if self.role.name.__contains__('service'):
            return True

    def __str__(self):
        return self.username
