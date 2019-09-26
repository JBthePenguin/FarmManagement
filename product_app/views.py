from django.shortcuts import render
from product_app.models import Product


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
    products = Product.objects.all()
    context = {
        "product": "active",
        "products": products,
    }
    return render(request, 'product_app/product.html', context)


def update_product(request, product_id):
    return render(request, 'product_app/update.html')
