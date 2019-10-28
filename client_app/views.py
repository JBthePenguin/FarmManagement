from django.shortcuts import render, redirect, HttpResponse
from django.db.models.deletion import ProtectedError
from client_app.models import *
from client_app.forms import *


def client(request):
    """ client view used to:
    - display table with all client's category saved
    - display table with all client saved
    - delete a category or a client with ajax post request """
    if request.method == 'POST' and request.is_ajax():
        # ajax post
        action = request.POST.get('action')
        if action == "delete category":
            # delete category
            category_id = request.POST.get('category_id')
            category = CategoryClient.objects.get(pk=category_id)
            try:
                category.delete()
            except ProtectedError:
                # No delete because a client use this category
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
                # No delete because this client have order(s)
                return HttpResponse("Ce client ne peut pas être supprimé car une (ou des) commande(s) lui appartien(nen)t.")
            else:
                return HttpResponse("")
    # get all clients and  categories
    categories = CategoryClient.objects.all().order_by('name')
    clients = Client.objects.all().order_by('category__name', 'name')
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Clients",
        "client": "active",
        "categories": categories,
        "clients": clients,
    }
    return render(request, 'client_app/client.html', context)


def add_category(request):
    """ add a category view used to:
    - display form to add a client's category
    - save category in db """
    # form for CategoryClient
    form = CategoryForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        # category has added
        if form.is_valid():
            # save category in db
            form.save()
            return redirect('client')
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Ajouter une catégorie de client",
        "client": "active",
        "form": form,
    }
    return render(request, 'client_app/add_category.html', context)


def update_category(request, category_id):
    """ update a category view
    - display form to update a category
    - save changes in db """
    # form for update a category with his values in inputs values
    category = CategoryClient.objects.get(pk=category_id)
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == 'POST':
        # category has updated
        if form.is_valid():
            form.save()  # save category updated in db
            return redirect('client')
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Modifier une catégorie de client",
        "client": "active",
        "form": form,
    }
    return render(request, 'client_app/update_category.html', context)


def add_client(request):
    """ add a client view used to:
    - display form to add a client
    - save client in db """
    # form for Client
    form = ClientForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        # product has added
        if form.is_valid():
            form.save()  # save client in db
            return redirect('client')
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Ajouter un client",
        "client": "active",
        "form": form,
    }
    return render(request, 'client_app/add_client.html', context)


def update_client(request, client_id):
    """ update a client view
    - display form to update a client
    - save changes in db """
    # form for update a client with his values in inputs values
    client = Client.objects.get(pk=client_id)
    form = ClientForm(request.POST or None, instance=client)
    if request.method == 'POST':
        # client has updated
        if form.is_valid():
            form.save()  # save client updated in db
            return redirect('client')
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Modifier un client",
        "client": "active",
        "form": form,
    }
    return render(request, 'client_app/update_client.html', context)
