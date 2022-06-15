from django.contrib import admin
from .models import Signaux, Annonce,Notifications
from .models import Catégorie

# Register your models here.
admin.site.register(Signaux)
admin.site.register(Notifications)
admin.site.register(Catégorie)

admin.site.register(Annonce)