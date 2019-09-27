from django.shortcuts import render, redirect, HttpResponse
from product_app.models import Product
from product_app.forms import ProductForm


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
    context = {
        "product": "active",
        "products": products,
    }
    return render(request, 'product_app/product.html', context)


def add_product(request):
    """ add a product view """
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        # product has added
        if form.is_valid():
            form.save()
            return redirect('product')
    context = {
        "product": "active",
        "form": form,
    }
    return render(request, 'product_app/add_product.html', context)


def update_product(request, product_id):
    """ update a product view """
    product = Product.objects.get(pk=product_id)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == 'POST':
        # product has updated
        if form.is_valid():
            form.save()
            return redirect('product')
    context = {
        "product": "active",
        "form": form,
    }
    return render(request, 'product_app/update.html', context)
