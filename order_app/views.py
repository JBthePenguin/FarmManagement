from django.shortcuts import render, redirect
from django.utils import timezone
from order_app.models import Order, OrderBasket
from order_app.forms import OrderForm
from basket_app.models import BasketCategory, Basket, BasketProduct
from price_app.models import Price


def order(request):
    """ index view """
    orders_in_preparation = Order.objects.filter(
        status="en préparation").order_by('creation_date').reverse()
    orders_in_course_delivery = Order.objects.filter(
        status="en livraison").order_by('validation_date').reverse()
    orders_delivered = Order.objects.filter(
        status="livrée").order_by('delivery_date').reverse()
    composition = OrderBasket.objects.all()
    context = {
        "order": "active",
        "orders_in_preparation": orders_in_preparation,
        "orders_in_course_delivery": orders_in_course_delivery,
        "orders_delivered": orders_delivered,
        "composition": composition,
    }
    return render(request, 'order_app/order.html', context)


def create_order(request):
    form = OrderForm(request.POST or None, request.FILES or None)
    categories_basket = BasketCategory.objects.all().order_by('name')
    baskets = Basket.objects.all().order_by('number')
    if request.method == 'POST':
        # order has created
        if form.is_valid():
            order = form.save()
            for category in categories_basket:
                quantity = request.POST.get("quantity" + category.name)
                basket_number = request.POST.get(str(category.id))
                if quantity != "" and basket_number != "":
                    basket = Basket.objects.get(number=basket_number)
                    component = OrderBasket(
                        order=order,
                        basket=basket,
                        quantity_basket=quantity)
                    component.save()
                print(quantity, " numéro ", basket_number)
            return redirect('order')
    context = {
        "order": "active",
        "form": form,
        "categories_basket": categories_basket,
        "baskets": baskets,
    }
    return render(request, 'order_app/create_order.html', context)


def validate_order(request, order_id):
    order_created = Order.objects.get(pk=order_id)
    composition = OrderBasket.objects.filter(
        order=order_created).order_by("basket__category__name")
    compositions_basket = {}
    products = []
    for component in composition:
        composition_basket = BasketProduct.objects.filter(
            basket=component.basket)
        compositions_basket[component.basket.number] = composition_basket
        for component_basket in composition_basket:
            products.append(component_basket.product)
    products = list(set(products))
    prices = Price.objects.filter(
        category_client=order_created.client.category,
        product__in=products)
    total_prices = {}
    for key, value in compositions_basket.items():
        total_price = 0
        for composition_basket in value:
            for price in prices:
                if composition_basket.product == price.product:
                    total_price += round(
                        price.value * composition_basket.quantity_product, 2)
        total_prices[key] = total_price
    if request.method == 'POST':
        # order is validated
        order_created.validation_date = timezone.now()
        order_created.status = "en livraison"
        order_created.save()
        return redirect('order')
    context = {
        "order": "active",
        "order_created": order_created,
        "composition": composition,
        "compositions_basket": compositions_basket,
        "prices": prices,
        "total_prices": total_prices,
    }
    return render(request, 'order_app/validate_order.html', context)
