from django.shortcuts import render, redirect, HttpResponse
from cost_app.models import CostCategory
from cost_app.forms import CostCategoryForm


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
            category.delete()
            return HttpResponse("")
    # get all categories by calcul mode
    categories_percent = CostCategory.objects.filter(
        calcul_mode="percent").order_by("name")
    categories_quantity = CostCategory.objects.filter(
        calcul_mode="quantity").order_by("name")
    # prepare and send all elements needed to construct the template
    context = {
        "page_title": "| Coûts",
        "cost": "active",
        "categories_percent": categories_percent,
        "categories_quantity": categories_quantity,
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
