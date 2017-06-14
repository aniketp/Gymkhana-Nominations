import django_filters
from .models import Nomination


class NominationFilter(django_filters.FilterSet):
    class Meta:
        model = Nomination
        fields = ['club_search__club', 'year_choice']
