from django.shortcuts import render, redirect, HttpResponse
from django.db.models.deletion import ProtectedError
from basket_app.models import Basket, BasketCategory, BasketProduct
from basket_app.forms import *
from product_app.models import Product
from client_app.models import CategoryClient
from price_app.models import Price
from order_app.models import OrderBasket


def basket(request):
    """ basket view used to:
    - display table with all client's category saved
    - display table with all client saved
    - delete a category or a client with ajax post request """
    if request.method == 'POST' and request.is_ajax():
        # ajax post
        action = request.POST.get('action')
        if action == "delete category":
            # delete category
            category_id = request.POST.get('category_id')
            category = BasketCategory.objects.get(pk=category_id)
            try:
                category.delete()
            except ProtectedError:
                # No delete because this category have a basket created
                return HttpResponse("Cette catégorie ne peut pas être supprimée car un (ou des) panier(s) lui appartien(nen)t.")
            else:
                return HttpResponse("")
        elif action == "delete basket":
            # delete basket
            basket_id = request.POST.get('basket_id')
            basket = Basket.objects.get(pk=basket_id)
            try:
                basket.delete()
            except ProtectedError:
                # No delete because this basket is used in order in preparation
                return HttpResponse("Ce panier ne peut pas être supprimé car il appartient à une (ou des) commande(s) en préparation.")
            else:
                # update all basket's numbers
                baskets = Basket.objects.all().order_by('number')
                number = 1
                for basket in baskets:
                    basket.number = number
                    basket.save()
                    number += 1
                return HttpResponse("")
    # get all baskets, basket's categories, compositons,
    # client's categories and prices
    baskets = Basket.objects.all().order_by('number')
    categories = BasketCategory.objects.all().order_by('name')
    compositions = BasketProduct.objects.all().order_by(
        'basket__number', 'product__name')
    categories_client = CategoryClient.objects.all().order_by('name')
    prices = Price.objects.all()
    # make a dict for total price by basket for each client's category
    # {basket number: total prices by client's category}
    total_prices_by_basket = {}
    for basket in baskets:
        # make a dict for total price by client's category
        # {client's category name: total price}
        total_prices_by_category = {}
        for category in categories_client:
            total_price = 0
            for component in compositions:
                if component.basket == basket:
                    for price in prices:
                        if (
                            (price.product == component.product) and (
                                price.category_client == category)):
                            total_price += round(
                                price.value * component.quantity_product, 2)
            total_prices_by_category[category.name] = total_price
        total_prices_by_basket[basket.number] = total_prices_by_category
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Paniers",
        "basket": "active",
        "baskets": baskets,
        "categories": categories,
        "compositions": compositions,
        "categories_client": categories_client,
        "prices": prices,
        "total_prices": total_prices_by_basket,
    }
    return render(request, 'basket_app/basket.html', context)


def add_category_basket(request):
    """ add a category view used to:
    - display form to add a basket's category
    - save category in db """
    # form for BasketCategory
    form = BasketCategoryForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        # category basket has added
        if form.is_valid():
            # save category in db
            form.save()
            return redirect('basket')
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Ajouter une catégorie de paniers",
        "basket": "active",
        "form": form,
    }
    return render(request, 'basket_app/add_category_basket.html', context)


def update_category_basket(request, category_id):
    """ update a category view
    - display form to update a category
    - save changes in db """
    # form for update a category with his values in inputs values
    category = BasketCategory.objects.get(pk=category_id)
    form = BasketCategoryForm(request.POST or None, instance=category)
    if request.method == 'POST':
        # category has updated
        if form.is_valid():
            form.save()  # save category updated in db
            return redirect('basket')
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Modifier une catégorie de panier",
        "basket": "active",
        "form": form,
    }
    return render(request, 'basket_app/update_category_basket.html', context)


def create_basket(request):
    """ basket view """
    form = BasketForm(request.POST or None, request.FILES or None)
    basket_number = Basket.objects.all().count() + 1
    products = Product.objects.all().order_by('name')
    if request.method == 'POST':
        # basket has added
        if form.is_valid():
            basket = form.save(commit=False)
            basket.number = basket_number
            basket.save()
            for product in products:
                quantity = request.POST.get(product.name)
                if quantity != "":
                    component = BasketProduct(
                        basket=basket,
                        product=product,
                        quantity_product=quantity)
                    component.save()
            return redirect('basket')
    context = {
        "basket": "active",
        "form": form,
        "basket_number": basket_number,
        "products": products,
    }
    return render(request, 'basket_app/create_basket.html', context)


def update_basket(request, basket_number):
    basket = Basket.objects.get(number=basket_number)
    old_basket_category = basket.category
    msg = ""
    form = BasketForm(request.POST or None, instance=basket)
    products = Product.objects.all().order_by('name')
    composition = {}
    for product in products:
        try:
            component = BasketProduct.objects.get(
                basket=basket, product=product)
            quantity = str(component.quantity_product)
        except BasketProduct.DoesNotExist:
            quantity = ""
        composition[product.name] = quantity
    if request.method == 'POST':
        # basket has updated
        if form.is_valid():
            try:
                OrderBasket.objects.get(basket=basket)
            except OrderBasket.DoesNotExist:
                basket = form.save(commit=False)
                basket.number = basket_number
                basket.save()
                for product in products:
                    new_quantity = request.POST.get(product.name)
                    try:
                        component = BasketProduct.objects.get(
                            basket=basket, product=product)
                        quantity = str(component.quantity_product)
                        if quantity != new_quantity:
                            if new_quantity == "":
                                component.delete()
                            else:
                                component.quantity_product = new_quantity
                                component.save()
                    except BasketProduct.DoesNotExist:
                        if new_quantity != "":
                            component = BasketProduct(
                                basket=basket,
                                product=product,
                                quantity_product=new_quantity)
                            component.save()
                return redirect('basket')
            else:
                new_basket_category = form.instance.category
                if old_basket_category != new_basket_category:
                    # raise error because basket is used in an created order
                    msg = "Ce panier ne peut pas changer de catégorie car il appartient à une commande en préparation."
                    basket.category = old_basket_category
                    form = BasketForm(None, instance=basket)
                    composition = {}
                    for product in products:
                        quantity = request.POST.get(product.name)
                        composition[product.name] = quantity
                else:
                    basket = form.save(commit=False)
                    basket.number = basket_number
                    basket.save()
                    for product in products:
                        new_quantity = request.POST.get(product.name)
                        try:
                            component = BasketProduct.objects.get(
                                basket=basket, product=product)
                            quantity = str(component.quantity_product)
                            if quantity != new_quantity:
                                if new_quantity == "":
                                    component.delete()
                                else:
                                    component.quantity_product = new_quantity
                                    component.save()
                        except BasketProduct.DoesNotExist:
                            if new_quantity != "":
                                component = BasketProduct(
                                    basket=basket,
                                    product=product,
                                    quantity_product=new_quantity)
                                component.save()
                    return redirect('basket')
    context = {
        "basket": "active",
        "basket_number": basket_number,
        "form": form,
        "products": products,
        "composition": composition,
        "msg": msg,
    }
    return render(request, 'basket_app/update_basket.html', context)
