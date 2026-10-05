from django import template

register = template.Library()


@register.filter
def startswith(value, arg):
    return str(value).startswith(arg)


@register.filter
def to_str(value):
    if value is None:
        return ''
    return str(value)
