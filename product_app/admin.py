from django.contrib import admin
from product_app.models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Model for product in admin site """
    list_display = ('id', 'name', 'unit')


@admin.register(ProductOrdered)
class ProductOrderedAdmin(admin.ModelAdmin):
    """ Model for product ordered in admin site """
    list_display = ('id', 'name', 'unit')
