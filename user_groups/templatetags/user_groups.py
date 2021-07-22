from django import template
from django.template.defaultfilters import stringfilter
from accounts.models import AerpawUser

register = template.Library()

@register.filter
@stringfilter
def role_name(role):
    if role == 'site_admin':
        return 'is Administrator'
    elif role == 'operator':
        return 'is Operator'
    elif role == 'project_manager':
        return 'can Create Projects'
    elif role == 'resource_manager':
        return 'can Manage Resources'
    elif role == 'aerpaw_user':
        return 'is AERPAW User'
    elif role == 'user_manager':
        return 'can Manage User Roles'
    else:
        return role


@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)


@register.filter
def displayname_by_id(user_id):
    return AerpawUser.objects.get(id=int(user_id)).display_name
