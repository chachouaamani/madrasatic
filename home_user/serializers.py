

from rest_framework import serializers
from .models import Catégorie , Annonce , Signaux

class CatégorieSerializer (serializers.ModelSerializer):
    class Meta :
        model = Catégorie
        fields= '__all__'


class AnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = '__all__'


class SignauxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signaux
        fields = '__all__'