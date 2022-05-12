
# Create your models here.

from django.db import models
from users.models import Users
from home_user.models import Signaux
import datetime
import os.path

def filepath(request,filename):
    old_filename=filename
    timeNow=datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename="%s%s" %(timeNow,old_filename)
    return os.path.join('uploads/',filename)

class Rapport(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    signalement= models.ForeignKey(Signaux, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, null=False, default="anything")
    description = models.TextField(max_length=500,null=False, default="anything")
    date = models.DateField()
    validate = models.BooleanField(default=False)
    send = models.BooleanField(default=False)
    image = models.ImageField(null=False, blank=True, upload_to=filepath)
    complement = models.CharField(null=False, default="anything", max_length=200)

    def __str__(self):
        return self.title






