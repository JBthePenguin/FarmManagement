from django.contrib import admin
from cost_app.models import CostCategory


@admin.register(CostCategory)
class CostCategoryAdmin(admin.ModelAdmin):
    """ Model for cost's category in admin site """
    list_display = ('id', 'name', 'calcul_mode')
