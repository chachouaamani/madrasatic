
from django.db import models
from users.models import Users
import datetime
import os

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

# Create your models here.

class Declaration(models.Model):
    User = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, null=False, default="anything")
    description = models.CharField(max_length=250, null=False, default="anything")
    date = models.DateField()
    post_date = models.DateTimeField(auto_now_add=True)
    place = models.CharField(max_length=250, null=False, default="anything")
    category = models.CharField(null=False, default="anything", max_length=50)
    validete = models.BooleanField(default=False)
    image = models.ImageField(null=False, blank=True, upload_to=filepath)

