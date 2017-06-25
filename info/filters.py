import django_filters
from nomi.models import Post


class PostFilter(django_filters.FilterSet):
    post_name = django_filters.ModelChoiceFilter(queryset=Post.objects.all())

    class Meta:
        model = Post
        fields = ['post_name', 'club_search__club']
