from .models import POST,UserProfile

def context(request):
    if request.user.is_authenticated:
        my_profile = UserProfile.objects.get(request.user)
        my_posts = Post.objects.filter(post_holders=request.user)
        return {'my_posts':my_posts,'my_profile':my_profile}
    else:
        return None