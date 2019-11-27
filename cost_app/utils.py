from order_app.models import BasketProductOrdered, BasketOrdered
from product_app.models import ProductOrdered
from cost_app.models import AdditionalCostProduct, AdditionalCost


def get_total_revenue():
    """ return total revenue: sum of total price of delivered order """
    baskets_ordered = BasketOrdered.objects.filter(
        order__status="livrée")
    total_revenue = 0
    for basket in baskets_ordered:
        products_ordered = BasketProductOrdered.objects.filter(
            basket=basket)
        for product in products_ordered:
            price = basket.quantity * product.quantity_product * product.price_product
            total_revenue += price
    return total_revenue


def get_total_by_products():
    """ return a dict
    key: product ordered
    value: (total_quantity, total_price)"""
    products_ordered = ProductOrdered.objects.all().order_by("name")
    total_by_products = {}
    for product in products_ordered:
        products_delivered = BasketProductOrdered.objects.filter(
            basket__order__status="livrée", product=product)
        total_quantity = 0
        total_price = 0
        for product_delivered in products_delivered:
            quantity = product_delivered.quantity_product * product_delivered.basket.quantity
            total_quantity += quantity
            price = quantity * product_delivered.price_product
            total_price += price
        if total_quantity != 0:
            if str(total_quantity)[-2:] == ".0":
                total_quantity = int(str(total_quantity)[:-2])
            total_by_products[product] = (total_quantity, total_price)
    return total_by_products


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
