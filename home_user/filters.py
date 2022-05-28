import django_filters
from .models import Signaux


class OrderFilter(django_filters.FilterSet):

    class Meta:
        model=Signaux
        fields = ['statut']