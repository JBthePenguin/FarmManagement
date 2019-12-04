from django import template
from order_app.models import OrderBasket, BasketOrdered, BasketProductOrdered
from basket_app.templatetags.basket_display import get_basket_total_price

register = template.Library()


@register.filter
def get_composition_order(order):
    """ return the compsition for a specific order """
    return OrderBasket.objects.filter(order=order).order_by(
        "basket__category__name")


@register.filter
def get_total_price_order(order):
    """ return the total price for a specific order """
    composition = OrderBasket.objects.filter(order=order)
    total_price_order = 0
    for component in composition:
        total_price_basket = get_basket_total_price(
            component.basket, order.client.category)
        if total_price_basket != "":
            total_price_order += total_price_basket * component.quantity_basket
    if total_price_order == 0:
        return ""
    return total_price_order


@register.filter
def get_composition_order_validated(order):
    """ return the compsition for a specific order """
    return BasketOrdered.objects.filter(order=order).order_by("category_name")


@register.filter
def get_composition_basket_ordered(basket):
    """ return the compsition for a specific basket ordered """
    return BasketProductOrdered.objects.filter(basket=basket).order_by(
        "product__name")


@register.filter
def get_basket_ordered_total_price(basket):
    """ return the compsition for a specific basket ordered """
    compositon = BasketProductOrdered.objects.filter(basket=basket)
    total_price = 0
    for component in compositon:
        total_price += round(
            component.price_product * component.quantity_product, 2)
    if total_price == 0:
        return ""
    return total_price


@register.filter
def get_total_price_order_validated(order):
    """ return the total price for a specific order """
    composition = BasketOrdered.objects.filter(order=order)
    total_price_order = 0
    for basket in composition:
        total_price_basket = get_basket_ordered_total_price(basket)
        if total_price_basket != "":
            total_price_order += total_price_basket * basket.quantity
    if total_price_order == 0:
        return ""
    return total_price_order
