from django.contrib import admin
from product_app.models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit')


@admin.register(ProductOrdered)
class ProductOrderedAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit')
