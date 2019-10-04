from django.shortcuts import render, redirect, HttpResponse
from django.db.models.deletion import ProtectedError
from basket_app.models import Basket, BasketCategory
from basket_app.forms import *


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
    context = {
        "basket": "active",
        "baskets": baskets,
        "categories": categories,
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
    context = {
        "basket": "active",
    }
    return render(request, 'basket_app/create_basket.html', context)
