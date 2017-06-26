from django import template

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
