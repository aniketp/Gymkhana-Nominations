import django_filters
from nomi.models import UserProfile


class UserProfileFilter(django_filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = ['club__tag_name', 'post__post_name']