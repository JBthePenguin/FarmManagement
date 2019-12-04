from django import template
from cost_app.models import Cost

register = template.Library()


@register.filter
def get_costs_by_category(category):
    return Cost.objects.filter(category=category).order_by("name")
