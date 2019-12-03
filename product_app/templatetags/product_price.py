from django import template
from price_app.models import Price

register = template.Library()


@register.filter
def get_price(product, category_client):
    """ return price of a product for a specific client's category """
    try:
        price = Price.objects.get(
            product=product, category_client=category_client)
    except Price.DoesNotExist:
        return ""
    else:
        return price.value


@register.filter
def get_price_amount(product, category_client):
    """ return price amount of a product for a specific client's category """
    try:
        price = Price.objects.get(
            product=product, category_client=category_client)
    except Price.DoesNotExist:
        return ""
    else:
        return str(price.value.amount)
