from django.shortcuts import render, redirect, HttpResponse
from djmoney.money import Money
from product_app.models import Product
from product_app.forms import ProductForm
from client_app.models import CategoryClient
from price_app.models import Price


def index(request):
    """ index view """
    return render(request, 'product_app/index.html')


def product(request):
    """ product view """
    if request.method == 'POST' and request.is_ajax():
        action = request.POST.get('action')
        if action == "delete":
            # delete product
            product_id = request.POST.get('product_id')
            product = Product.objects.get(pk=product_id)
            product.delete()
            return HttpResponse("")
    products = Product.objects.all().order_by('name')
    categories_client = CategoryClient.objects.all().order_by('name')
    prices = Price.objects.all()
    context = {
        "product": "active",
        "products": products,
        "categories_client": categories_client,
        "prices": prices,
    }
    return render(request, 'product_app/product.html', context)


def add_product(request):
    """ add a product view """
    form = ProductForm(request.POST or None, request.FILES or None)
    categories_client = CategoryClient.objects.all().order_by('name')
    if request.method == 'POST':
        # product has added
        if form.is_valid():
            form.save()
            product = Product.objects.get(name=form.instance.name)
            for category_client in categories_client:
                price_value = request.POST.get(category_client.name)
                if price_value != "":
                    price = Price(
                        product=product,
                        category_client=category_client,
                        value=price_value)
                    price.save()
            return redirect('product')
    context = {
        "product": "active",
        "form": form,
        "categories_client": categories_client,
    }
    return render(request, 'product_app/add_product.html', context)


def update_product(request, product_id):
    """ update a product view """
    product = Product.objects.get(pk=product_id)
    form = ProductForm(request.POST or None, instance=product)
    categories_client = CategoryClient.objects.all().order_by('name')
    prices = {}
    for category_client in categories_client:
        try:
            price = Price.objects.get(
                product=product, category_client=category_client)
            price_value = str(price.value.amount)
        except Price.DoesNotExist:
            price_value = ""
        prices[category_client.name] = price_value
    if request.method == 'POST':
        # product has updated
        if form.is_valid():
            form.save()
            for category_client in categories_client:
                new_price_value = request.POST.get(category_client.name)
                try:
                    price = Price.objects.get(
                        product=product, category_client=category_client)
                    price_value = str(price.value.amount)
                    if price_value != new_price_value:
                        if new_price_value == "":
                            price.delete()
                        else:
                            price.value = Money(new_price_value, 'EUR')
                            price.save()
                except Price.DoesNotExist:
                    if new_price_value != "":
                        price = Price(
                            product=product,
                            category_client=category_client,
                            value=new_price_value)
                        price.save()
            return redirect('product')
    context = {
        "product": "active",
        "form": form,
        "categories_client": categories_client,
        "prices": prices,
    }
    return render(request, 'product_app/update_product.html', context)
