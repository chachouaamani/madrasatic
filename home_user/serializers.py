from rest_framework import serializers

from home_user.models import Signaux, Catégorie, Annonce

class SignauxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signaux
        fields = '__all__'

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catégorie
        fields = '__all__'

class AnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = '__all__'