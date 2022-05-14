import datetime
from datetime import date

from django.db import models
from users.models import Users,Service
import os


def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)


# Create your models here.
class Catégorie(models.Model):
    name = models.CharField(max_length=50, default="None", unique=True)
    image = models.ImageField(null=False, blank=True, upload_to=filepath)
    description = models.TextField(max_length=30, default="none")

    def __str__(self):
        return self.name


class Signaux(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)
    titre = models.CharField(max_length=50, default="none", null=False)
    category = models.ForeignKey(Catégorie, on_delete=models.CASCADE, default=1)
    lieu = models.CharField(max_length=100, default="None", null=False)
    date = models.DateField(null=False)
    heure = models.TimeField(null=False)
    description = models.TextField(max_length=200, default="None", null=False)
    send = models.BooleanField(default=False)
    validate = models.BooleanField(default=False)
    statut = models.CharField(max_length=50, default="non_traité")
    complement = models.CharField(null=True, default="anything", max_length=200)
    service=models.ForeignKey(Service,on_delete=models.CASCADE, default=1)
    image = models.ImageField(null=False, blank=True, upload_to=filepath)

    def __str__(self):
        return self.titre




class Annonce(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    titre = models.CharField(max_length=50, null=False, default="anything")
    image = models.ImageField(null=False, blank=True, upload_to=filepath)
    description = models.TextField(max_length=200)
    date_debut = models.DateField(null=False)
    date_fin = models.DateField(null=False)
    validate = models.BooleanField(default=False)
    status = models.CharField(max_length=255, null=False, default="non_valider")



    @property
    def equal(self):
        if self.date_debut <= date.today() <= self.date_fin:
            return True

    def __str__(self):
        return self.titre
