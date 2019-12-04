from django.shortcuts import render, redirect, HttpResponse
from django.utils import timezone
from order_app.models import *
from order_app.forms import OrderForm
from order_app.utils import get_products_client
from cost_app.utils import get_total_revenue, get_total_by_products
from basket_app.models import BasketCategory, Basket, BasketProduct
from price_app.models import Price


def order(request):
    """ order view used to:
    - display table with orders ordered by status and date
    - delete or cancel an order with ajax post request """
    if request.method == 'POST' and request.is_ajax():
        # ajax post
        action = request.POST.get('action')
        if action == "delete order" or action == "cancel order":
            # delete order
            order_id = request.POST.get('order_id')
            order = Order.objects.get(pk=order_id)
            order.delete()
            return HttpResponse("")
    # get all orders by status, all compositions and all baskets ordered
    orders_in_preparation = Order.objects.filter(
        status="en préparation").order_by('creation_date').reverse()
    orders_in_course_delivery = Order.objects.filter(
        status="en livraison").order_by('validation_date').reverse()
    orders_delivered = Order.objects.filter(
        status="livrée").order_by('delivery_date').reverse()
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "Commandes",
        "order": "active",
        "orders_in_preparation": orders_in_preparation,
        "orders_in_course_delivery": orders_in_course_delivery,
        "orders_delivered": orders_delivered,
    }
    return render(request, 'order_app/order.html', context)


def create_order(request):
    """ create an order view
    - display form to create an order
    - save order and composition in db """
    # form for create an order
    form = OrderForm(request.POST or None, request.FILES or None)
    # get all basket's categories
    categories_basket = BasketCategory.objects.all().order_by('name')
    if request.method == 'POST':
        # order has created
        if form.is_valid():
            order = form.save()  # save order with default status
            for category in categories_basket:
                quantity = request.POST.get("quantity" + category.name)
                basket_number = request.POST.get(str(category.id))
                if quantity != "" and basket_number != "":
                    basket = Basket.objects.get(number=basket_number)
                    component = OrderBasket(
                        order=order,
                        basket=basket,
                        quantity_basket=quantity)
                    component.save()  # save composition
            return redirect('order')
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "Créer une commande",
        "order": "active",
        "form": form,
        "categories_basket": categories_basket,
    }
    return render(request, 'order_app/create_order.html', context)


def update_order(request, order_id):
    """ update an order view
    - display form to update an order
    - save changes in db """
    # form for update a client with his values in inputs values
    order_created = Order.objects.get(pk=order_id)
    form = OrderForm(request.POST or None, instance=order_created)
    # get all basket's categories
    categories_basket = BasketCategory.objects.all().order_by('name')
    # make a dict for composition', "" if no basket of this category in order
    # {basket's category name: component}
    composition_by_category = {}
    for category in categories_basket:
        composition_by_category[category] = ""
        composition = OrderBasket.objects.filter(
            order=order_created, basket__category=category)
        for component in composition:
            composition_by_category[category] = component
    if request.method == 'POST':
        # order has updated
        if form.is_valid():
            order = form.save()  # save order
            for category in categories_basket:
                component = composition_by_category[category]
                new_quantity = request.POST.get("quantity" + category.name)
                new_basket_number = request.POST.get(str(category.id))
                if (component == "") and (new_quantity != "") and (
                        new_basket_number != ""):
                    basket = Basket.objects.get(number=new_basket_number)
                    component = OrderBasket(
                        order=order,
                        basket=basket,
                        quantity_basket=new_quantity)
                    component.save()  # save composition
                elif component != "":
                    if new_quantity == "" or new_basket_number == "":
                        component.delete()  # delete composition
                    elif (new_quantity != str(component.quantity_basket)) or (
                            new_basket_number != str(component.basket.number)):
                        component.quantity_basket = new_quantity
                        basket = Basket.objects.get(number=new_basket_number)
                        component.basket = basket
                        component.save()  # save composition
            # origin request
            origin_address = request.POST.get("origin-address")
            return redirect(origin_address)
    # origin request
    try:
        origin_address = request.META['HTTP_REFERER']
    except KeyError:
        origin_address = "/commandes/"
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "Modifier une commande",
        "order": "active",
        "order_created": order_created,
        "form": form,
        "categories_basket": categories_basket,
        "composition_by_category": composition_by_category,
        "origin_address": origin_address,
    }
    return render(request, 'order_app/update_order.html', context)


def validate_order(request, order_id):
    """ validate an order view
    - display tables with baskets ordered with prices for an order and
    button link to validate this order
    - save new status (order validated) in db """
    # get order created
    order_created = Order.objects.get(pk=order_id)
    if request.method == 'POST':
        # order is validated
        order_created.validation_date = timezone.now()
        order_created.status = "en livraison"
        order_created.save()  # save new status
        # get composition of order
        composition_order = OrderBasket.objects.filter(order=order_created)
        for component_order in composition_order:
            basket_ordered = BasketOrdered(
                order=order_created,
                category_name=component_order.basket.category.name,
                quantity=component_order.quantity_basket)
            basket_ordered.save()  # save in basket ordered
            composition_basket = BasketProduct.objects.filter(
                basket=component_order.basket)
            for component_basket in composition_basket:
                price = Price.objects.get(
                    product=component_basket.product,
                    category_client=order_created.client.category)
                composition_basket_ordered = BasketProductOrdered(
                    basket=basket_ordered,
                    product=component_basket.product,
                    quantity_product=component_basket.quantity_product,
                    price_product=price.value)
                # save in composition basket ordered
                composition_basket_ordered.save()
            component_order.delete()  # delete in composition basket
        # origin request
        origin_address = request.POST.get("origin-address")
        return redirect(origin_address)
    # origin request
    try:
        origin_address = request.META['HTTP_REFERER']
    except KeyError:
        origin_address = "/commandes/"
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "Valider une commande",
        "order": "active",
        "order_created": order_created,
        "origin_address": origin_address,
    }
    return render(request, 'order_app/validate_order.html', context)


def deliver_order(request, order_id):
    """ deliver an order view
    - display tables with baskets with prices for an order validated and
    button link to deliverer this order
    - save new status (order delivered) in db """
    # get order validated
    order_validated = Order.objects.get(pk=order_id)
    if request.method == 'POST':
        # order is validated
        order_validated.delivery_date = timezone.now()
        order_validated.status = "livrée"
        order_validated.save()  # update status in db
        # origin request
        origin_address = request.POST.get("origin-address")
        return redirect(origin_address)
    # origin request
    try:
        origin_address = request.META['HTTP_REFERER']
    except KeyError:
        origin_address = "/commandes/"
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "Livrer une commande",
        "order": "active",
        "order_validated": order_validated,
        "origin_address": origin_address,
    }
    return render(request, 'order_app/deliver_order.html', context)


def delivered_order(request, order_id):
    """ order delivered view
    - display tables with baskets with prices for an order delivered """
    # get order delivered
    order_delivered = Order.objects.get(pk=order_id)
    # origin request
    try:
        origin_address = request.META['HTTP_REFERER']
    except KeyError:
        origin_address = "/commandes/"
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "Commande livrée",
        "order": "active",
        "order_delivered": order_delivered,
        "origin_address": origin_address,
    }
    return render(request, 'order_app/delivered_order.html', context)


def client_orders(request, client_id):
    """ client's orders view used to:
    - display table with a client's orders ordered by status and date
    - delete or cancel an order with ajax post request """
    if request.method == 'POST' and request.is_ajax():
        # ajax post
        action = request.POST.get('action')
        if action == "delete order" or action == "cancel order":
            # delete order
            order_id = request.POST.get('order_id')
            order = Order.objects.get(pk=order_id)
            order.delete()
            return HttpResponse("")
    # get client
    client = Client.objects.get(pk=client_id)
    # get all orders for this client
    # by status, all compositions and all baskets ordered
    orders_in_preparation = Order.objects.filter(
        client=client, status="en préparation").order_by(
            'creation_date').reverse()
    orders_in_course_delivery = Order.objects.filter(
        client=client, status="en livraison").order_by(
            'validation_date').reverse()
    orders_delivered = Order.objects.filter(
        client=client, status="livrée").order_by(
            'delivery_date').reverse()
    # get total gain for the client
    products_client = get_products_client(client)
    total_gain = 0
    for key, value in products_client.items():
        total_gain += value[1]
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "Commandes - " + client.name,
        "client": "active",
        "client_name": client.name,
        "orders_in_preparation": orders_in_preparation,
        "orders_in_course_delivery": orders_in_course_delivery,
        "orders_delivered": orders_delivered,
        "total_revenue": get_total_revenue(),
        "total_by_products": get_total_by_products(),
        "products_client": products_client,
        "total_gain": total_gain,
    }
    return render(request, 'order_app/client_orders.html', context)
