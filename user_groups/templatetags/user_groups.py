from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def role_name(role):
    if role == 'site-admin':
        return 'is Administrator'
    elif role == 'operator':
        return 'is Operator'
    elif role == 'project-manager':
        return 'can Create Projects'
    elif role == 'resource-manager':
        return 'can Manage Resources'
    elif role == 'aerpaw-user':
        return 'is AERPAW User'
    elif role == 'user-manager':
        return 'can Manage User Roles'
    else:
        return role


@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)
