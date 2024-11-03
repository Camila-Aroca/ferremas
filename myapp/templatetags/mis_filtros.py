from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplica el valor por el argumento."""
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0
