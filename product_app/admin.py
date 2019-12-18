from django.contrib import admin
from product_app.models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Model for product in admin site """
    list_display = ('id', 'name', 'unit')
