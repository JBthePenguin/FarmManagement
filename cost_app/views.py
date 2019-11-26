from django.shortcuts import render, redirect, HttpResponse
from django.db.models.deletion import ProtectedError
from cost_app.models import (
    CostCategory, Cost, AdditionalCost, AdditionalCostProduct)
from cost_app.forms import CostCategoryForm, CostForm
from cost_app.utils import (
    get_total_revenue, get_total_by_products, get_total_cost_product)
from product_app.models import Product


def cost(request):
    """ cost view used to:
    - display table with all costs ordered by calcul mode and category
    - display table with all client saved
    - delete a category or a cost with ajax post request """
    if request.method == 'POST' and request.is_ajax():
        # ajax post
        action = request.POST.get('action')
        if action == "delete category":
            # delete category
            category_id = request.POST.get('category_id')
            category = CostCategory.objects.get(pk=category_id)
            try:
                category.delete()
            except ProtectedError:
                # No delete because a cost use this category
                return HttpResponse("Cette catégorie ne peut pas être supprimée car des coûts lui appartiennent.")
            else:
                return HttpResponse("")
        elif action == "delete cost":
            # delete cost
            cost_id = request.POST.get('cost_id')
            cost = Cost.objects.get(pk=cost_id)
            cost.delete()
            return HttpResponse("")
    # get all categories by calcul mode
    categories_percent = CostCategory.objects.filter(
        calcul_mode="percent").order_by("name")
    categories_quantity = CostCategory.objects.filter(
        calcul_mode="quantity").order_by("name")
    # get all costs by categories calcul mode
    costs_percent = Cost.objects.filter(
        category__calcul_mode="percent").order_by("category__name", "name")
    costs_quantity = Cost.objects.filter(
        category__calcul_mode="quantity").order_by("category__name", "name")
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Coûts",
        "cost": "active",
        "categories_percent": categories_percent,
        "categories_quantity": categories_quantity,
        "costs_percent": costs_percent,
        "costs_quantity": costs_quantity,
    }
    return render(request, 'cost_app/cost.html', context)


def add_cost_category(request, calcul_mode):
    """ add a cost category view used to
    - display form to add a cost category
    - save category with calcul mode in db """
    # form for Cost Category
    form = CostCategoryForm(request.POST or None, request.FILES or None)
    form.fields['calcul_mode'].initial = calcul_mode
    if request.method == 'POST':
        # category cost has added
        if form.is_valid():
            # save category in db
            form.save()
            return redirect('cost')
    context = {
        "page_title": "| Ajouter une catégorie de coût",
        "cost": "active",
        "form": form,
        'calcul_mode': calcul_mode,
    }
    return render(request, 'cost_app/add_cost_category.html', context)


def update_category_cost(request, category_id):
    """ update a cost category view
    - display form to update a category
    - save changes in db """
    # form for update a category with his values in inputs values
    category = CostCategory.objects.get(pk=category_id)
    form = CostCategoryForm(request.POST or None, instance=category)
    if request.method == 'POST':
        # category has updated
        if form.is_valid():
            form.save()  # save category updated in db
            return redirect('cost')
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Modifier une catégorie de coût",
        "cost": "active",
        "form": form,
        'calcul_mode': category.calcul_mode,
    }
    return render(request, 'cost_app/update_category_cost.html', context)


def add_cost(request, category_id):
    """ add a cost view used to
    - display form to add a cost
    - save cost with category in db """
    # form for Cost
    form = CostForm(request.POST or None, request.FILES or None)
    form.fields['category'].initial = category_id
    # get cost's category
    category = CostCategory.objects.get(pk=category_id)
    if request.method == 'POST':
        # category cost has added
        if form.is_valid():
            # save cost in db
            form.save()
            return redirect('cost')
    context = {
        "page_title": "| Ajouter un coût",
        "cost": "active",
        "form": form,
        "cost_category": category.name,
        "calcul_mode": category.calcul_mode,
    }
    return render(request, 'cost_app/add_cost.html', context)


def update_cost(request, cost_id):
    """ update a cost view
    - display form to update a cost
    - save changes in db """
    # form for update a cost with his values in inputs values
    cost = Cost.objects.get(pk=cost_id)
    form = CostForm(request.POST or None, instance=cost)
    if request.method == 'POST':
        # cost has updated
        if form.is_valid():
            form.save()  # save cost updated in db
            return redirect('cost')
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Modifier un coût",
        "cost": "active",
        "form": form,
        "cost_category": cost.category.name,
        "calcul_mode": cost.category.calcul_mode,
    }
    return render(request, 'cost_app/update_cost.html', context)


def calcul(request):
    """ calculate cost percent with revenue and cost per product
    - display total revenue and table with revenue for each product
    - display tables for each general cost
    - display table with total cost per product
    """
    # get all general categories with costs and their quantities
    general_categories = CostCategory.objects.filter(
        calcul_mode="percent").order_by("name")
    general_costs = Cost.objects.filter(
        category__calcul_mode="percent").order_by("category__name", "name")
    general_cost_quantities = {}
    for cost in general_costs:
        additional_costs = AdditionalCost.objects.filter(cost=cost)
        quantity = 0
        for additional_cost in additional_costs:
            quantity += additional_cost.quantity
        if str(quantity)[-2:] == ".0":
            quantity = int(str(quantity)[:-2])
        general_cost_quantities[cost.id] = quantity
    # total by general category
    # make a dict: {category id: total}
    totals_by_general_category = {}
    for category in general_categories:
        additional_costs = AdditionalCost.objects.filter(
            cost__category=category)
        total = 0
        for additional_cost in additional_costs:
            total += additional_cost.quantity * additional_cost.cost.amount
        totals_by_general_category[category.id] = total
    # total for general costs
    total_general_costs = 0
    for category_id, total in totals_by_general_category.items():
        total_general_costs += total
    # get all products
    products = Product.objects.all().order_by("name")
    # total cost by product
    # make a dict: {product id: total}
    total_cost_by_product = {}
    for product in products:
        total_cost_by_product[product.id] = get_total_cost_product(product)
    # total for costs per product
    total_costs_product = 0
    for key, value in total_cost_by_product.items():
        total_costs_product += value
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Coûts et chiffre d'affaire",
        "cost": "active",
        "total_revenue": get_total_revenue(),
        "total_by_products": get_total_by_products(),
        "general_categories": general_categories,
        "general_costs": general_costs,
        "general_cost_quantities": general_cost_quantities,
        "totals_by_general_category": totals_by_general_category,
        'total_general_costs': total_general_costs,
        "products": products,
        "total_cost_by_product": total_cost_by_product,
        "total_costs_product": total_costs_product,
        "total_costs": total_costs_product + total_general_costs,
    }
    return render(request, 'cost_app/calcul.html', context)


def add_genaral_cost(request, cost_id):
    """ add a general cost view used to
    - display form to add a general cost and historical of added
    - save added cost in db """
    # get general cost
    general_cost = Cost.objects.get(pk=cost_id)
    if request.method == 'POST':
        if request.is_ajax():
            # ajax post
            action = request.POST.get('action')
            if action == "delete added cost":
                # delete added cost
                added_cost_id = request.POST.get('added_cost_id')
                added_cost = AdditionalCost.objects.get(pk=added_cost_id)
                added_cost.delete()
                return HttpResponse("")
        quantity = request.POST.get('added-quantity')
        additional_cost = AdditionalCost(
            cost=general_cost,
            quantity=quantity,)
        additional_cost.save()
        return redirect('calcul')
    # get added costs for general cost
    additional_costs = AdditionalCost.objects.filter(
        cost=general_cost).order_by("date_added").reverse()
    # get total quantity
    total_quantity = 0
    for additional_cost in additional_costs:
        total_quantity += additional_cost.quantity
    if str(total_quantity)[-2:] == ".0":
        total_quantity = int(str(total_quantity)[:-2])
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Mise à jour d'un coût",
        "cost": "active",
        "general_cost": general_cost,
        "additional_costs": additional_costs,
        "total_quantity": total_quantity,
    }
    return render(request, 'cost_app/add_general_cost.html', context)


def costs_per_product(request, product_id):
    """ costs per product view
    - display tables with all costs for one product """
    # get product, all costs per product and the categories    
    product = Product.objects.get(pk=product_id)
    cost_product_categories = CostCategory.objects.filter(
        calcul_mode="quantity").order_by("name")
    costs_product = Cost.objects.filter(
        category__calcul_mode="quantity").order_by("category__name", "name")
    # make a dict for quantities
    # {cost id: quantity}
    cost_product_quantities = {}
    for cost in costs_product:
        additional_costs_product = AdditionalCostProduct.objects.filter(
            additional_cost__cost=cost, product=product)
        quantity = 0
        for additional_cost_product in additional_costs_product:
            quantity += additional_cost_product.additional_cost.quantity
        if str(quantity)[-2:] == ".0":
            quantity = int(str(quantity)[:-2])
        cost_product_quantities[cost.id] = quantity
    # total by cost per product category
    # make a dict: {category id: total}
    totals_by_cost_product_category = {}
    for category in cost_product_categories:
        additional_costs_product = AdditionalCostProduct.objects.filter(
            additional_cost__cost__category=category, product=product)
        total = 0
        for additional_cost_product in additional_costs_product:
            total += additional_cost_product.additional_cost.quantity * additional_cost_product.additional_cost.cost.amount
        totals_by_cost_product_category[category.id] = total
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Coûts par produit",
        "cost": "active",
        "product": product,
        "total_costs": get_total_cost_product(product),
        "total_revenue": get_total_revenue(),
        "cost_product_categories": cost_product_categories,
        "costs_product": costs_product,
        "cost_product_quantities": cost_product_quantities,
        "totals_by_cost_product_category": totals_by_cost_product_category,
    }
    return render(request, 'cost_app/costs_per_product.html', context)


def add_cost_per_product(request, cost_id, product_id):
    """ add a general cost view used to
    - display form to add a general cost and historical of added
    - save added cost in db """
    # get general cost
    cost_per_product = Cost.objects.get(pk=cost_id)
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        if request.is_ajax():
            # ajax post
            action = request.POST.get('action')
            if action == "delete added cost":
                # delete added cost
                added_cost_id = request.POST.get('added_cost_id')
                added_cost = AdditionalCost.objects.get(pk=added_cost_id)
                added_cost.delete()
                return HttpResponse("")
        quantity = request.POST.get('added-quantity')
        additional_cost = AdditionalCost(
            cost=cost_per_product,
            quantity=quantity,)
        additional_cost.save()  # save additional cost
        additional_cost_product = AdditionalCostProduct(
            additional_cost=additional_cost,
            product=product)
        additional_cost_product.save()  # save additional cost product
        return redirect(
            '/couts/calcul/couts-par-produit/' + str(product_id) + '/')
    # get added costs for cost per product
    additional_costs_product = AdditionalCostProduct.objects.filter(
        additional_cost__cost=cost_per_product, product=product).order_by(
            "additional_cost__date_added").reverse()
    # get total quantity
    total_quantity = 0
    for additional_cost_product in additional_costs_product:
        total_quantity += additional_cost_product.additional_cost.quantity
    if str(total_quantity)[-2:] == ".0":
        total_quantity = int(str(total_quantity)[:-2])
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Mise à jour d'un coût",
        "cost": "active",
        "cost_per_product": cost_per_product,
        "product": product,
        "additional_costs_product": additional_costs_product,
        "total_quantity": total_quantity,
    }
    return render(request, 'cost_app/add_cost_product.html', context)
