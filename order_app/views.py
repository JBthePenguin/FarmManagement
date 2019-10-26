from django.shortcuts import render, redirect, HttpResponse
from django.db.utils import IntegrityError
from django.db.models.deletion import ProtectedError
from django.utils import timezone
from order_app.models import *
from order_app.forms import OrderForm
from basket_app.models import BasketCategory, Basket, BasketProduct
from price_app.models import Price
from product_app.models import ProductOrdered


def order(request):
    """ index view """
    if request.method == 'POST' and request.is_ajax():
        action = request.POST.get('action')
        if action == "delete order" or action == "cancel order":
            # delete or cancel category
            order_id = request.POST.get('order_id')
            order = Order.objects.get(pk=order_id)
            order.delete()
            if action == "cancel order":
                products_ordered = ProductOrdered.objects.all()
                for product_ordered in products_ordered:
                    try:
                        product_ordered.delete()
                    except ProtectedError:
                        pass
            return HttpResponse("")
    orders_in_preparation = Order.objects.filter(
        status="en préparation").order_by('creation_date').reverse()
    orders_in_course_delivery = Order.objects.filter(
        status="en livraison").order_by('validation_date').reverse()
    orders_delivered = Order.objects.filter(
        status="livrée").order_by('delivery_date').reverse()
    composition = OrderBasket.objects.all()
    baskets_ordered = BasketOrdered.objects.all().order_by("category_name")
    context = {
        "page_title": "| Commandes",
        "order": "active",
        "orders_in_preparation": orders_in_preparation,
        "orders_in_course_delivery": orders_in_course_delivery,
        "orders_delivered": orders_delivered,
        "composition": composition,
        "baskets_ordered": baskets_ordered,
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


def update_order(request, order_id):
    order_created = Order.objects.get(pk=order_id)
    baskets = Basket.objects.all().order_by('number')
    categories_basket = BasketCategory.objects.all().order_by('name')
    composition = OrderBasket.objects.filter(
        order=order_created).order_by("basket__category__name")
    composition_by_category = {}
    for category in categories_basket:
        composition_by_category[category.name] = ""
        for component in composition:
            if component.basket.category == category:
                composition_by_category[category.name] = component
    form = OrderForm(request.POST or None, instance=order_created)
    if request.method == 'POST':
        # basket has updated
        if form.is_valid():
            order = form.save()
            for category in categories_basket:
                component = composition_by_category[category.name]
                new_quantity = request.POST.get("quantity" + category.name)
                new_basket_number = request.POST.get(str(category.id))
                if (component == "") and (new_quantity != "") and (new_basket_number != ""):
                    basket = Basket.objects.get(number=new_basket_number)
                    component = OrderBasket(
                        order=order,
                        basket=basket,
                        quantity_basket=new_quantity)
                    component.save()
                elif component != "":
                    if new_quantity == "" or new_basket_number == "":
                        component.delete()
                    elif new_quantity != str(component.quantity_basket) or new_basket_number != str(component.basket.number):
                        component.quantity_basket = new_quantity
                        basket = Basket.objects.get(number=new_basket_number)
                        component.basket = basket
                        component.save()
            return redirect('order')
    context = {
        "order": "active",
        "order_created": order_created,
        "baskets": baskets,
        "form": form,
        "categories_basket": categories_basket,
        "composition_by_category": composition_by_category,
    }
    return render(request, 'order_app/update_order.html', context)


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
    order_price = 0
    for key, value in compositions_basket.items():
        total_price = 0
        for composition_basket in value:
            for price in prices:
                if composition_basket.product == price.product:
                    total_price += round(
                        price.value * composition_basket.quantity_product, 2)
        total_prices[key] = total_price
        for component in composition:
            if component.basket.number == key:
                order_price += total_price * component.quantity_basket
    if request.method == 'POST':
        # order is validated
        order_created.validation_date = timezone.now()
        order_created.status = "en livraison"
        order_created.save()
        # save in product ordered
        for product in products:
            try:
                product_ordered = ProductOrdered(
                    name=product.name,
                    unit=product.unit)
                product_ordered.save()
            except IntegrityError:
                pass
        for key, value in compositions_basket.items():
            # save in basket ordered
            basket = Basket.objects.get(number=key)
            composition_order = OrderBasket.objects.get(
                order=order_created, basket=basket)
            basket_ordered = BasketOrdered(
                order=order_created,
                category_name=basket.category.name,
                quantity=composition_order.quantity_basket)
            basket_ordered.save()
            for composition_basket in value:
                # save in composition basket ordered
                product_ordered = ProductOrdered.objects.get(
                    name=composition_basket.product.name,
                    unit=composition_basket.product.unit)
                price = Price.objects.get(
                    product=composition_basket.product,
                    category_client=order_created.client.category)
                composition_basket_ordered = BasketProductOrdered(
                    basket=basket_ordered,
                    product=product_ordered,
                    quantity_product=composition_basket.quantity_product,
                    price_product=price.value)
                composition_basket_ordered.save()
            composition_order.delete()
        return redirect('order')
    context = {
        "order": "active",
        "order_created": order_created,
        "composition": composition,
        "compositions_basket": compositions_basket,
        "prices": prices,
        "total_prices": total_prices,
        "order_price": order_price,
    }
    return render(request, 'order_app/validate_order.html', context)


def deliver_order(request, order_id):
    order_validated = Order.objects.get(pk=order_id)
    if request.method == 'POST':
        # order is validated
        order_validated.delivery_date = timezone.now()
        order_validated.status = "livrée"
        order_validated.save()
        return redirect('order')
    baskets_ordered = BasketOrdered.objects.filter(
        order=order_validated).order_by("category_name")
    compositions_basket = BasketProductOrdered.objects.filter(
        basket__in=baskets_ordered).order_by("product__name")
    total_prices = {}
    order_price = 0
    for basket in baskets_ordered:
        total_price = 0
        for component in compositions_basket:
            if component.basket == basket:
                total_price += round(
                    component.price_product * component.quantity_product, 2)
        total_prices[basket] = total_price
        order_price += total_price * basket.quantity
    context = {
        "order": "active",
        "order_validated": order_validated,
        "baskets_ordered": baskets_ordered,
        "compositions_basket": compositions_basket,
        "total_prices": total_prices,
        "order_price": order_price,
    }
    return render(request, 'order_app/deliver_order.html', context)


def delivered_order(request, order_id):
    order_delivered = Order.objects.get(pk=order_id)
    baskets_ordered = BasketOrdered.objects.filter(
        order=order_delivered).order_by("category_name")
    compositions_basket = BasketProductOrdered.objects.filter(
        basket__in=baskets_ordered).order_by("product__name")
    total_prices = {}
    order_price = 0
    for basket in baskets_ordered:
        total_price = 0
        for component in compositions_basket:
            if component.basket == basket:
                total_price += round(
                    component.price_product * component.quantity_product, 2)
        total_prices[basket] = total_price
        order_price += total_price * basket.quantity
    context = {
        "order": "active",
        "order_delivered": order_delivered,
        "baskets_ordered": baskets_ordered,
        "compositions_basket": compositions_basket,
        "total_prices": total_prices,
        "order_price": order_price,
    }
    return render(request, 'order_app/delivered_order.html', context)
