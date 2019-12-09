from django import template
from cost_app.models import Cost, AdditionalCost, AdditionalCostProduct

register = template.Library()


@register.filter
def get_costs_by_category(category):
    """ return all costs for a specific category """
    return Cost.objects.filter(category=category).order_by("name")


@register.filter
def get_cost_quantity(cost):
    """ return the total quantity for a specific cost """
    additional_costs = AdditionalCost.objects.filter(cost=cost)
    quantity = 0
    for additional_cost in additional_costs:
        quantity += additional_cost.quantity
    if str(quantity)[-2:] == ".0":
        quantity = int(str(quantity)[:-2])
    return quantity


@register.filter
def get_cost_quantity_per_product(cost, product):
    """ return the total quantity for a specific cost for a product """
    additional_costs_product = AdditionalCostProduct.objects.filter(
        additional_cost__cost=cost, product=product)
    quantity = 0
    for additional_cost_product in additional_costs_product:
        quantity += additional_cost_product.additional_cost.quantity
    if str(quantity)[-2:] == ".0":
        quantity = int(str(quantity)[:-2])
    return quantity
