from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def is_active(request, url):
    """
    Returns 'active' if the current URL matches the given URL pattern,
    otherwise returns an empty string.
    """
    if request.path == reverse(url):
        return 'active'
    return ''
