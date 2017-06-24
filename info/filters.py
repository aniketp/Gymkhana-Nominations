import django_filters
from nomi.models import Post


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['post_name', 'tag']
