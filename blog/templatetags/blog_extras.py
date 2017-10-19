from django.contrib.auth.models import Group
from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """ Check if user is in a particular group
    """
    try:
        group =  Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False

    return group in user.groups.all()