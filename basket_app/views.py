from django.shortcuts import render, redirect, HttpResponse
from django.db.models.deletion import ProtectedError
from basket_app.models import Basket, BasketCategory, BasketProduct
from basket_app.forms import *
from product_app.models import Product
from client_app.models import CategoryClient
from price_app.models import Price


def basket(request):
    """ basket view """
    if request.method == 'POST' and request.is_ajax():
        action = request.POST.get('action')
        if action == "delete category":
            # delete category
            category_id = request.POST.get('category_id')
            category = BasketCategory.objects.get(pk=category_id)
            try:
                category.delete()
            except ProtectedError:
                return HttpResponse("Cette catégorie ne peut pas être supprimée car des paniers lui appartiennent.")
            else:
                return HttpResponse("")
    baskets = Basket.objects.all().order_by('number')
    categories = BasketCategory.objects.all().order_by('name')
    compositions = BasketProduct.objects.all().order_by(
        'basket__number', 'product__name')
    categories_client = CategoryClient.objects.all().order_by('name')
    prices = Price.objects.all()
    total_prices_by_basket = {}
    for basket in baskets:
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
    context = {
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
    """ add category basket view """
    form = BasketCategoryForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        # product has added
        if form.is_valid():
            form.save()
            return redirect('basket')
    context = {
        "basket": "active",
        "form": form,
    }
    return render(request, 'basket_app/add_category_basket.html', context)


def update_category_basket(request, category_id):
    category = BasketCategory.objects.get(pk=category_id)
    form = BasketCategoryForm(request.POST or None, instance=category)
    if request.method == 'POST':
        # category has updated
        if form.is_valid():
            form.save()
            return redirect('basket')
    context = {
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
