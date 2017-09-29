from django import template
from nomi.models import Deratification

register = template.Library()

@register.filter
def to_class_name(value):
    return value.__class__.__name__




@register.filter
def group_status(group):
    out = False
    for nomi in group.nominations.all():
        if nomi.status == 'Nomination out':
            out = True
            break

    return out

@register.filter
def give_session(st_year):
    return str(st_year) + " - " + str(st_year+1)


@register.filter
def check_end_tenure(user,post):
    out = False
    derati = Deratification.objects.filter(post = post).filter(name = user).filter(status = 'end tenure')
    if derati:
        out = True

    return out

@register.filter
def check_remove_from_post(user,post):
    out = False
    derati = Deratification.objects.filter(post = post).filter(name = user).filter(status = 'remove from post')
    if derati:
        out = True

    return out