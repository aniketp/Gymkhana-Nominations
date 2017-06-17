from .models import Post, UserProfile
from django.core.exceptions import ObjectDoesNotExist


def context(request):
    if request.user.is_authenticated:
        try:
            my_profile = UserProfile.objects.get(user=request.user)
            my_posts = Post.objects.filter(post_holders=request.user)
            return {'my_posts': my_posts, 'my_profile': my_profile}
        except ObjectDoesNotExist:
            return {'my_posts': 0, 'my_profile': 0}
    else:
        return {'my_posts': 0, 'my_profile': 0}
