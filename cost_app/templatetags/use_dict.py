from django import template

register = template.Library()


@register.filter
def get_value(dictionnary, key):
    return dictionnary[key]
