import django_filters
from .models import UserProfile


class UserProfileFilter(django_filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = ['name', 'roll_no', 'year', 'programme', 'department', 'hall']


