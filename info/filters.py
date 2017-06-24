import django_filters
from nomi.models import Post, Club


def posts(request):
    if request is None:
        post = Post.objects.all()

    else:
        club_id = request.GET['club_search__club']
        club = Club.objects.get(pk=club_id)
        post = Post.objects.filter(club = club)

    return request.user


class PostFilter(django_filters.FilterSet):
    post_name = django_filters.ModelChoiceFilter(queryset=posts)

    class Meta:
        model = Post
        fields = ['post_name']
