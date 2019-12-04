from django import template

register = template.Library()


@register.filter
def get_value_in_dict(dictionnary, key):
    return dictionnary[key]
