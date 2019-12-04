from order_app.models import BasketProductOrdered
from product_app.models import Product


def get_products_client(client):
    """ return a dict
    key: product ordered by a client
    value: (total_quantity, total_price)"""
    products_ordered = Product.objects.all().order_by("name")
    total_by_products = {}
    for product in products_ordered:
        products_delivered = BasketProductOrdered.objects.filter(
            basket__order__client=client,
            basket__order__status="livrée", product=product)
        total_quantity = 0
        total_price = 0
        for product_delivered in products_delivered:
            quantity = product_delivered.quantity_product * product_delivered.basket.quantity
            total_quantity += quantity
            price = quantity * product_delivered.price_product
            total_price += price
        # if total_quantity != 0:
        total_by_products[product] = (total_quantity, total_price)
    return total_by_products
