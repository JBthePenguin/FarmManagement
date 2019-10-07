from django.shortcuts import render, redirect
from order_app.models import Order, OrderBasket
from order_app.forms import OrderForm
from basket_app.models import BasketCategory, Basket


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
