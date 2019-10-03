from django.contrib import admin
from basket_app.models import *


@admin.register(BasketCategory)
class BasketCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'categorie')


@admin.register(BasketProduct)
class BasketProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'basket', 'product', 'quantity_product')
