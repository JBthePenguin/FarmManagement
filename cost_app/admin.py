from django import forms
from django.contrib import admin
from cost_app.models import CostCategory, Cost, AdditionalCost


@admin.register(CostCategory)
class CostCategoryAdmin(admin.ModelAdmin):
    """ Model for cost's category in admin site """
    list_display = ('id', 'name', 'calcul_mode')


class CostCategoryModelChoiceField(forms.ModelChoiceField):
    """ Model to display cost's category's names in select cost's category
    for save a cost in admin site"""
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class CostAdminForm(forms.ModelForm):
    """ Form to save a cost in admin site"""
    category = CostCategoryModelChoiceField(
        queryset=CostCategory.objects.all())

    class Meta:
        model = Cost
        fields = "__all__"


@admin.register(Cost)
class CostAdmin(admin.ModelAdmin):
    """ Model for cost in admin site """
    form = CostAdminForm
    list_display = ('id', 'get_category_cost', 'name', 'amount', 'unit')

    def get_category_cost(self, obj):
        """ return the name of the cost's category
        for cost's table in admin site"""
        return "%s" % (obj.category.name)

    get_category_cost.short_description = 'Category cost'


class CostModelChoiceField(forms.ModelChoiceField):
    """ Model to display cost's category's names in select cost's category
    for save a cost in admin site"""
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class AdditionalCostAdminForm(forms.ModelForm):
    """ Form to save a cost in admin site"""
    cost = CostModelChoiceField(
        queryset=Cost.objects.all().order_by('name'))

    class Meta:
        model = AdditionalCost
        fields = "__all__"


@admin.register(AdditionalCost)
class AdditionalCostAdmin(admin.ModelAdmin):
    """ Model for cost in admin site """
    form = AdditionalCostAdminForm
    list_display = ('get_cost', 'quantity', 'date_added')

    def get_cost(self, obj):
        """ return the name of the cost's category
        for cost's table in admin site"""
        return "%s" % (obj.cost.name)

    get_cost.short_description = 'Cost'
