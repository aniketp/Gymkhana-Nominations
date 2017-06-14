import django_filters
from .models import Nomination


class NominationFilter(django_filters.FilterSet):
    class Meta:
        model = Nomination
        fields = ['nomi_approvals__club', 'year_choice']
