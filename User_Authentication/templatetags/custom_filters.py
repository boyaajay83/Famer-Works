from django import template

register = template.Library()

@register.filter
def toColor(status):
    """Returns 'green' if True, 'red' if False."""
    return "green" if status else "red"
