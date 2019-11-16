from django.shortcuts import render, redirect, HttpResponse
from django.db.models.deletion import ProtectedError
from cost_app.models import CostCategory, Cost
from cost_app.forms import CostCategoryForm, CostForm, CostUpdateForm
from cost_app.utils import get_total_revenue, get_total_by_products
from djmoney.money import Money


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
        "total_revenue": get_total_revenue(),
        "total_by_products": get_total_by_products(),
    }
    return render(request, 'cost_app/cost.html', context)


def add_cost_category(request, calcul_mode):
    """ add a cost category view used to
    - display form to add a cost category
    - save category with calcul mode in db """
    # form for Cost Category
    form = CostCategoryForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        # category cost has added
        if form.is_valid():
            # save category in db
            category = form.save(commit=False)
            category.calcul_mode = calcul_mode
            category.save()
            return redirect('cost')
    context = {
        "page_title": "| Ajouter une catégorie de coût",
        "cost": "active",
        "form": form,
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
    }
    return render(request, 'cost_app/update_category_cost.html', context)


def add_cost(request, category_id):
    """ add a cost view used to
    - display form to add a cost
    - save cost with category in db """
    # form for Cost
    form = CostForm(request.POST or None, request.FILES or None)
    # get cost's category
    category = CostCategory.objects.get(pk=category_id)
    if request.method == 'POST':
        # category cost has added
        if form.is_valid():
            # save category in db
            cost = form.save(commit=False)
            cost.category = category
            cost.save()
            return redirect('cost')
    context = {
        "page_title": "| Ajouter un coût",
        "cost": "active",
        "form": form,
        "cost_category": category.name,
    }
    return render(request, 'cost_app/add_cost.html', context)


def update_cost(request, cost_id):
    """ update a cost view
    - display form to update a cost
    - save changes in db """
    # form for update a cost with his values in inputs values
    cost = Cost.objects.get(pk=cost_id)
    form = CostUpdateForm(request.POST or None, instance=cost)
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

    }
    return render(request, 'cost_app/update_cost.html', context)


def calcul_percent(request):
    """ calculate cost percent with revenue
    - display form to calculate costs
    """
    # get all categories and costs for this calcul mode
    categories = CostCategory.objects.filter(
        calcul_mode="percent").order_by("name")
    costs = Cost.objects.filter(
        category__calcul_mode="percent").order_by("category__name", "name")
    cost_quantities = {}
    total_revenue = False
    totals_by_category = {}
    total_costs = 0
    if request.method == 'POST':
        # calculate
        i = 0
        for cost in costs:
            # get cost's value
            cost_quantity = request.POST.get(str(cost.id))
            if cost_quantity == "":
                i += 1
            cost_quantities[cost.id] = cost_quantity
        if i == len(cost_quantities):
            # no cost's value
            cost_quantities = {}
        # get total revenue
        total_revenue = request.POST.get("total-revenue")
        if total_revenue == "0":
            # total revenue is 0
            total_revenue = False
        else:
            total_revenue = Money(total_revenue, 'EUR')
        if total_revenue is not False and len(cost_quantities) != 0:
            # calculate total cost by category
            for category in categories:
                total = 0
                for cost in costs:
                    if cost.category == category:
                        quantity = cost_quantities[cost.id]
                        if quantity != "":
                            total += (cost.amount * quantity)
                totals_by_category[category.id] = total
            for category, total in totals_by_category.items():
                total_costs += total
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Calculer coût en pourcentage du chiffre d'affaire",
        "cost": "active",
        "categories": categories,
        "costs": costs,
        "cost_quantities": cost_quantities,
        "total_revenue": total_revenue,
        "totals_by_category": totals_by_category,
        'total_costs': total_costs,
    }
    return render(request, 'cost_app/calculate_percent.html', context)


def calcul_quantity(request):
    """ calculate cost with product's quantity
    - display form to calculate costs
    """
    # get all categories and costs for this calcul mode
    categories = CostCategory.objects.filter(
        calcul_mode="quantity").order_by("name")
    costs = Cost.objects.filter(
        category__calcul_mode="quantity").order_by("category__name", "name")
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Calculer coût par rapport à la quantité de produits",
        "cost": "active",
        "categories": categories,
        "costs": costs,
    }
    return render(request, 'cost_app/calculate_quantity.html', context)
