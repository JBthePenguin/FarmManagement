from django.shortcuts import render, redirect, HttpResponse
from django.db.models.deletion import ProtectedError
from client_app.models import *
from client_app.forms import *


def client(request):
    """ index view """
    if request.method == 'POST' and request.is_ajax():
        action = request.POST.get('action')
        if action == "delete category":
            # delete product
            category_id = request.POST.get('category_id')
            category = CategoryClient.objects.get(pk=category_id)
            try:
                category.delete()
            except ProtectedError:
                return HttpResponse("Cette catégorie ne peut pas être supprimée car des clients lui appartiennent.")
            else:
                return HttpResponse("")
    categories = CategoryClient.objects.all().order_by('name')
    context = {
        "client": "active",
        "categories": categories,
    }
    return render(request, 'client_app/client.html', context)


def add_category(request):
    form = CategoryForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        # product has added
        if form.is_valid():
            form.save()
            return redirect('client')
    context = {
        "client": "active",
        "form": form,
    }
    return render(request, 'client_app/add_category.html', context)


def update_category(request, category_id):
    category = CategoryClient.objects.get(pk=category_id)
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == 'POST':
        # category has updated
        if form.is_valid():
            form.save()
            return redirect('client')
    context = {
        "client": "active",
        "form": form,
    }
    return render(request, 'client_app/update_category.html', context)
