import sys
from django.core.management import call_command
from django.shortcuts import render, redirect, HttpResponse
from django.db.models.deletion import ProtectedError
from djmoney.money import Money
from product_app.models import Product
from product_app.forms import ProductForm
from client_app.models import CategoryClient
from price_app.models import Price


def index(request):
    """ index view """
    msg = ""
    if request.method == 'POST':
        # dump db
        sysout = sys.stdout
        sys.stdout = open('db_save.json', 'w')
        call_command(
            'dumpdata', 'product_app', 'client_app',
            'basket_app', 'price_app', 'order_app', 'cost_app')
        sys.stdout = sysout
        msg = "Données sauvegardées"
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "Accueil",
        "msg": msg,
    }
    return render(request, 'product_app/index.html', context)


def product(request):
    """ product view used to:
    - display table with all products saved
        (name, unit and price for each client's category)
    - delete a product with ajax post request """
    if request.method == 'POST' and request.is_ajax():
        # ajax post
        action = request.POST.get('action')
        if action == "delete":
            # get product
            product_id = request.POST.get('product_id')
            product = Product.objects.get(pk=product_id)
            try:
                # delete product in db
                product.delete()
            except ProtectedError:
                # No delete because product is used in a basket
                return HttpResponse("".join([
                    "Ce produit ne peut pas être supprimé",
                    " car il appartient à un (ou des) panier(s) ",
                    ", ou a une commande validée ou à des coûts."]))
            else:
                # product deleted
                return HttpResponse("")
    # get all products, client's categories
    products = Product.objects.all().order_by('name')
    categories_client = CategoryClient.objects.all().order_by('name')
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "Produits",
        "product": "active",
        "products": products,
        "categories_client": categories_client,
    }
    return render(request, 'product_app/product.html', context)


def add_product(request):
    """ add a product view used to
    - display form to add a product
    - save product with prices in db """
    # form for Product and client's_category needed for Price
    form = ProductForm(request.POST or None, request.FILES or None)
    categories_client = CategoryClient.objects.all().order_by('name')
    if request.method == 'POST':
        # product has added
        if form.is_valid():
            product = form.save()  # save product in db
            for category_client in categories_client:
                price_value = request.POST.get(category_client.name)
                if price_value != "":
                    # save price in db
                    price = Price(
                        product=product,
                        category_client=category_client,
                        value=price_value)
                    price.save()
            return redirect('product')
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "Ajouter produit",
        "product": "active",
        "form": form,
        "categories_client": categories_client,
    }
    return render(request, 'product_app/add_product.html', context)


def update_product(request, product_id):
    """ update a product view
    - display form to update a product
    - save changes in db """
    # form for update a product with his values in inputs values
    product_updated = Product.objects.get(pk=product_id)
    form = ProductForm(request.POST or None, instance=product_updated)
    categories_client = CategoryClient.objects.all().order_by('name')
    if request.method == 'POST':
        # product has updated
        if form.is_valid():
            form.save()  # save product updated in db
            for category_client in categories_client:
                new_price_value = request.POST.get(category_client.name)
                try:
                    price = Price.objects.get(
                        product=product_updated,
                        category_client=category_client)
                    price_value = str(price.value.amount)
                    if price_value != new_price_value:
                        # price changed
                        if new_price_value == "":
                            # delete price in db
                            price.delete()
                        else:
                            # save new price in db
                            price.value = Money(new_price_value, 'EUR')
                            price.save()
                except Price.DoesNotExist:
                    if new_price_value != "":
                        # save new price in db
                        price = Price(
                            product=product_updated,
                            category_client=category_client,
                            value=new_price_value)
                        price.save()
            return redirect('product')
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "Modifier produit",
        "product": "active",
        "product_updated": product_updated,
        "form": form,
        "categories_client": categories_client,
    }
    return render(request, 'product_app/update_product.html', context)
