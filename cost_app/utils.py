from order_app.models import BasketProductOrdered, Order
from product_app.models import Product
from cost_app.models import AdditionalCostProduct, AdditionalCost
from order_app.templatetags.order_display import (
    get_total_price_order_validated)


def get_total_revenue():
    """ return total revenue: sum of total price of delivered order """
    orders = Order.objects.filter(status="livrée")
    total_revenue = 0
    for order in orders:
        total_price_order = get_total_price_order_validated(order)
        if total_price_order != "":
            total_revenue += total_price_order
    return total_revenue


def get_total_by_products():
    """ return a dict
    key: product ordered
    value: (total_quantity, total_price)"""
    products = Product.objects.all().order_by("name")
    total_by_products = {}
    for product in products:
        components = BasketProductOrdered.objects.filter(
            basket__order__status="livrée", product=product)
        total_quantity = 0
        total_price = 0
        for component in components:
            quantity = component.quantity_product * component.basket.quantity
            total_quantity += quantity
            price = quantity * component.price_product
            total_price += price
        if total_quantity != 0:
            if str(total_quantity)[-2:] == ".0":
                total_quantity = int(str(total_quantity)[:-2])
        total_by_products[product] = (total_quantity, total_price)
    return total_by_products


def get_total_by_category(category):
    """ return total cost for a specific category """
    additional_costs = AdditionalCost.objects.filter(
        cost__category=category)
    total = 0
    for additional_cost in additional_costs:
        total += additional_cost.quantity * additional_cost.cost.amount
    return total


def get_total_cost_product(product):
    """ return total cost for a product """
    additional_costs_product = AdditionalCostProduct.objects.filter(
        product=product)
    total = 0
    for additional_cost_product in additional_costs_product:
        total += additional_cost_product.additional_cost.quantity * additional_cost_product.additional_cost.cost.amount
    return total


def get_totals_by_costs_product_category(cost_product_categories):
    """ return a dict
    {category id: total}"""
    totals_by_costs_product_category = {}
    for category in cost_product_categories:
        additional_costs = AdditionalCost.objects.filter(
            cost__category=category)
        total = 0
        for additional_cost in additional_costs:
            total += additional_cost.quantity * additional_cost.cost.amount
        totals_by_costs_product_category[category.id] = total
    return totals_by_costs_product_category
