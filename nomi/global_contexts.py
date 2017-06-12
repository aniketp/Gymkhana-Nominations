from .models import POST,UserProfile

def context(request):
    if request.user.is_authenticated:


    return {'notice':notice,'note':note}