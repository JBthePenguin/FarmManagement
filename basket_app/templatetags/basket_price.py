from django import template
from basket_app.models import Basket, BasketProduct
from price_app.models import Price

register = template.Library()


@register.filter
def get_baskets(category):
    """ return all baskets for a specific basket's category """
    return Basket.objects.filter(category=category).order_by("number")


@register.filter
def get_composition(basket):
    """ return the compsition for a specific basket """
    return BasketProduct.objects.filter(basket=basket).order_by(
        "product__name")


@register.filter
def get_basket_total_price(basket, category_client):
    """ return the compsition for a specific basket """
    composition = BasketProduct.objects.filter(basket=basket)
    total_price = 0
    for component in composition:
        try:
            price = Price.objects.get(
                product=component.product, category_client=category_client)
        except Price.DoesNotExist:
            pass
        else:
            total_price += round(price.value * component.quantity_product, 2)
    if total_price == 0:
        return ""
    else:
        return total_price
