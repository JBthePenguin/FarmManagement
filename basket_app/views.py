from django.shortcuts import render, redirect, HttpResponse
from django.db.models.deletion import ProtectedError
from basket_app.models import Basket, BasketCategory, BasketProduct
from basket_app.forms import *
from product_app.models import Product
from client_app.models import CategoryClient
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
                return HttpResponse("".join([
                    "Cette catégorie ne peut pas être supprimée",
                    " car un (ou des) panier(s) lui appartien(nen)t."]))
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
                return HttpResponse("".join([
                    "Ce panier ne peut pas être supprimé",
                    " car il appartient à une (ou des) commande(s)",
                    " en préparation."]))
            else:
                # update all basket's numbers
                baskets = Basket.objects.all().order_by('number')
                number = 1
                for basket in baskets:
                    if basket.number != number:
                        basket.number = number
                        basket.save()
                    number += 1
                return HttpResponse("")
    # get basket's categories, number of baskets and client's categories
    categories = BasketCategory.objects.all().order_by('name')
    number_of_baskets = Basket.objects.all().count()
    categories_client = CategoryClient.objects.all().order_by('name')
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "Paniers",
        "basket": "active",
        "categories": categories,
        "number_of_baskets": number_of_baskets,
        "categories_client": categories_client,
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
        "page_title": "Ajouter une catégorie de paniers",
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
        "page_title": "Modifier une catégorie de paniers",
        "basket": "active",
        "form": form,
    }
    return render(request, 'basket_app/update_category_basket.html', context)


def create_basket(request):
    """ create a basket view
    - display form to create a basket
    - save basket and composition in db """
    # form for create a basket
    form = BasketForm(request.POST or None, request.FILES or None)
    # set new basket number and get all products
    basket_number = Basket.objects.all().count() + 1
    products = Product.objects.all().order_by('name')
    if request.method == 'POST':
        # basket has created
        if form.is_valid():
            # save basket in db
            basket = form.save(commit=False)
            basket.number = basket_number
            basket.save()
            for product in products:
                quantity = request.POST.get(product.name)
                if quantity != "":
                    # save composion in db
                    component = BasketProduct(
                        basket=basket,
                        product=product,
                        quantity_product=quantity)
                    component.save()
            return redirect('basket')
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "Créer un panier",
        "basket": "active",
        "form": form,
        "basket_number": basket_number,
        "products": products,
    }
    return render(request, 'basket_app/create_basket.html', context)


def update_basket(request, basket_number):
    """ update a basket view
    - display form to update a basket
    - save changes in db """
    # form for update a client with his values in inputs values
    basket = Basket.objects.get(number=basket_number)
    form = BasketForm(request.POST or None, instance=basket)
    # make a dict for composition's values with "" if not
    # {product name: quantity}
    products = Product.objects.all().order_by('name')
    composition = {}
    for product in products:
        try:
            component = BasketProduct.objects.get(
                basket=basket, product=product)
            quantity = str(component.quantity_product)
        except BasketProduct.DoesNotExist:
            quantity = ""
        composition[product] = quantity
    # error message
    old_basket_category = basket.category
    msg = ""
    if request.method == 'POST':
        # basket has updated
        if form.is_valid():
            def save_basket_changes():
                """ save changes of basket updated """
                basket = form.save(commit=False)
                basket.number = basket_number
                basket.save()  # save basket in db
                for product in products:
                    # new quantity for each product
                    new_quantity = request.POST.get(product.name)
                    try:
                        # composition exist
                        component = BasketProduct.objects.get(
                            basket=basket, product=product)
                        quantity = str(component.quantity_product)
                        if quantity != new_quantity:
                            if new_quantity == "":
                                component.delete()  # delete composition row
                            else:
                                component.quantity_product = new_quantity
                                component.save()  # save new compositon in db
                    except BasketProduct.DoesNotExist:
                        # composition does not exist
                        if new_quantity != "":
                            component = BasketProduct(
                                basket=basket,
                                product=product,
                                quantity_product=new_quantity)
                            component.save()  # save new compositon in db
                return redirect('basket')
            try:
                OrderBasket.objects.get(basket=basket)
            except OrderBasket.DoesNotExist:
                # basket not used in an order
                return save_basket_changes()
            else:
                # basket used in an order
                new_basket_category = form.instance.category
                if old_basket_category != new_basket_category:
                    # raise error because basket is used in an created order
                    msg = "".join([
                        "Ce panier ne peut pas changer de catégorie car ",
                        "il appartient à une commande en préparation."])
                    basket.category = old_basket_category
                    # form for update a client with old values in inputs values
                    form = BasketForm(None, instance=basket)
                    # dict for composition's values
                    composition = {}
                    for product in products:
                        quantity = request.POST.get(product.name)
                        composition[product] = quantity
                else:
                    return save_basket_changes()
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "Modifier un panier",
        "basket": "active",
        "basket_number": basket_number,
        "form": form,
        "products": products,
        "composition": composition,
        "msg": msg,
    }
    return render(request, 'basket_app/update_basket.html', context)
