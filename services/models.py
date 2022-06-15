
# Create your models here.

from django.db import models
from users.models import Users
from home_user.models import Signaux,Signaux_archivé
import datetime
import os.path

def filepath(request,filename):
    old_filename=filename
    timeNow=datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename="%s%s" %(timeNow,old_filename)
    return os.path.join('uploads/',filename)

class Rapport(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    signalement= models.ForeignKey(Signaux, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=150, null=False, default="anything")
    description = models.TextField(null=False, default="anything")
    date = models.DateField()
    validate = models.BooleanField(default=False)
    status = models.CharField(null=False, default="Non_traité", max_length=20)
    image = models.ImageField(null=False, blank=True, upload_to=filepath)
    complement = models.CharField(null=False, default="anything", max_length=200)
    send = models.BooleanField(default=False)



    @property
    def valider(self):
        if self.validate==True:
            return True

    @property
    def sent(self):
        if self.send == True:
            return True

    def __str__(self):
        return self.title



class Rapport_archivé(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    signalement= models.ForeignKey(Signaux_archivé, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=150, null=False, default="anything")
    description = models.TextField(null=False, default="anything")
    date = models.DateField()
    validate = models.BooleanField(default=False)
    status = models.CharField(null=False, default="Non_traité", max_length=20)
    image = models.ImageField(null=False, blank=True, upload_to=filepath)
    complement = models.CharField(null=False, default="anything", max_length=200)
    send = models.BooleanField(default=False)



    def __str__(self):
        return self.title




class notifyrapp(models.Model):
    to_user=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='touserr',null=True)
    from_user = models.ForeignKey(Users, on_delete=models.CASCADE,related_name='fromuserr' ,null=True)
    message = models.TextField(max_length=2000)
    rap = models.ForeignKey(Rapport,  on_delete=models.CASCADE, null=True)

