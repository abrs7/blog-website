from django import template

register = template.Library()

@register.filter(name='first_upper')
def first_upper(value):
    return value[0].upper() + value[1:]
