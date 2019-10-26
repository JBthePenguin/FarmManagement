from django.shortcuts import render, redirect, HttpResponse
from django.db.models.deletion import ProtectedError
from client_app.models import *
from client_app.forms import *


def client(request):
    """ index view """
    if request.method == 'POST' and request.is_ajax():
        action = request.POST.get('action')
        if action == "delete category":
            # delete category
            category_id = request.POST.get('category_id')
            category = CategoryClient.objects.get(pk=category_id)
            try:
                category.delete()
            except ProtectedError:
                return HttpResponse("Cette catégorie ne peut pas être supprimée car des clients lui appartiennent.")
            else:
                return HttpResponse("")
        elif action == "delete client":
            # delete client
            client_id = request.POST.get('client_id')
            client = Client.objects.get(pk=client_id)
            try:
                client.delete()
            except ProtectedError:
                return HttpResponse("Ce client ne peut pas être supprimé car une (ou des) commande(s) lui appartien(nen)t.")
            else:
                return HttpResponse("")
    categories = CategoryClient.objects.all().order_by('name')
    clients = Client.objects.all().order_by('category__name', 'name')
    context = {
        "page_title": "| Clients",
        "client": "active",
        "categories": categories,
        "clients": clients,
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


def add_client(request):
    form = ClientForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        # product has added
        if form.is_valid():
            form.save()
            return redirect('client')
    context = {
        "client": "active",
        "form": form,
    }
    return render(request, 'client_app/add_client.html', context)


def update_client(request, client_id):
    client = Client.objects.get(pk=client_id)
    form = ClientForm(request.POST or None, instance=client)
    if request.method == 'POST':
        # category has updated
        if form.is_valid():
            form.save()
            return redirect('client')
    context = {
        "client": "active",
        "form": form,
    }
    return render(request, 'client_app/update_client.html', context)
