from django import template

register = template.Library()


@register.filter
def range_r(value):
    return range(value)


@register.filter
def subtract(value, arg):
    return value - arg
