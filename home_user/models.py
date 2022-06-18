import datetime
from datetime import date
from django.db import models
from users.models import Users, Service
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
    description = models.TextField(max_length=20, default="none")
    service = models.ForeignKey(Service, on_delete=models.RESTRICT, default=1)

    def __str__(self):
        return self.name



class Signaux(models.Model):
    STATUS=(
        ('Traité','Traité'),
        ('En_cours' ,'En_cours'),
        ('Non_traité', 'Non_traité'),
        ('Rejeté', 'Rejeté')
    )
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)
    titre = models.CharField(max_length=50, default="none", null=False)
    category = models.ForeignKey(Catégorie, on_delete=models.RESTRICT, default=1)
    lieu = models.CharField(max_length=100, default="None", null=False)
    salle = models.CharField(max_length=100, default="None", null=False)
    date = models.DateField(null=False)
    heure = models.TimeField(null=False)
    description = models.TextField(max_length=500, default="None", null=False)
    send = models.BooleanField(default=False)
    validate = models.BooleanField(default=False)
    statut = models.CharField(max_length=50, default="Non_traité",choices=STATUS)
    complement = models.CharField(null=True, default="anything", max_length=200)
    service = models.ForeignKey(Service, on_delete=models.RESTRICT, default=1)
    image = models.ImageField(null=False, blank=True, upload_to=filepath)
    rapport_ajouter = models.BooleanField(default=False)
    rattacher=models.BooleanField(default=False)
    pere=models.IntegerField(default=0)


    @property
    def sent(self):
        if self.send:
            return True

    @property
    def rapportajouter(self):
        if self.rapport_ajouter:
            return True

    def __str__(self):
        return self.titre



class Annonce(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    titre = models.CharField(max_length=50, null=False, default="anything")
    image = models.ImageField(null=False, blank=True, upload_to=filepath)
    description = models.TextField()
    date_debut = models.DateField(null=False)
    date_fin = models.DateField(null=False)
    validate = models.BooleanField(default=False)
    send = models.BooleanField(default=False)
    status = models.CharField(max_length=255, null=False, default="Non_traité")

    @property
    def equal(self):
        if self.date_debut <= date.today() <= self.date_fin:
            return True

    @property
    def sent(self):
        if self.send == True:
            return True

    def __str__(self):
        return self.titre

class Notifications(models.Model):
    to_user=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='to_user',null=True)
    from_user = models.ForeignKey(Users, on_delete=models.CASCADE,related_name='from_user' ,null=True)
    message = models.TextField(max_length=2000)
    sig = models.ForeignKey(Signaux,  on_delete=models.CASCADE, null=True)
class notify(models.Model):
    to_user=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='touser',null=True)
    from_user = models.ForeignKey(Users, on_delete=models.CASCADE,related_name='fromuser' ,null=True)
    message = models.TextField(max_length=2000)
    an = models.ForeignKey(Annonce,  on_delete=models.CASCADE, null=True)




class Signaux_archivé(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)
    titre = models.CharField(max_length=50, default="none", null=False)
    category = models.ForeignKey(Catégorie, on_delete=models.RESTRICT, default=1)
    lieu = models.CharField(max_length=100, default="None", null=False)
    salle = models.CharField(max_length=100, default="None", null=False)
    date = models.DateField(null=False)
    heure = models.TimeField(null=False)
    description = models.TextField(max_length=500, default="None", null=False)
    send = models.BooleanField(default=False)
    validate = models.BooleanField(default=False)
    statut = models.CharField(max_length=50, default="Non_traité")
    service = models.ForeignKey(Service, on_delete=models.RESTRICT, default=1)
    image = models.ImageField(null=False, blank=True, upload_to=filepath)
    rapport_ajouter = models.BooleanField(default=False)
    rattacher = models.BooleanField(default=False)
    pere = models.IntegerField(default=0)


    def __str__(self):
        return self.titre

