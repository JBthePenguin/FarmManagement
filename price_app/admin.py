from django import forms
from django.contrib import admin
from price_app.models import Price
from product_app.models import Product
from client_app.models import CategoryClient


class ProductModelChoiceField(forms.ModelChoiceField):
    """ Model to display product's names in select product
    for save a price in admin site"""
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class CategoryModelChoiceField(forms.ModelChoiceField):
    """ Model to display client's category's names in select client's category
    for save a price in admin site"""
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class PriceAdminForm(forms.ModelForm):
    """ Form to save a client in admin site"""
    product = CategoryModelChoiceField(
        queryset=Product.objects.all())
    category_client = CategoryModelChoiceField(
        queryset=CategoryClient.objects.all())

    class Meta:
        model = Price
        fields = "__all__"


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    """ Model for price in admin site """
    form = PriceAdminForm
    list_display = ('get_product', 'get_category_client', 'value')

    def get_product(self, obj):
        """ return the name of the product for price's table in admin site"""
        return "%s" % (obj.product.name)

    def get_category_client(self, obj):
        """ return the name of the client's category
        for price's table in admin site"""
        return "%s" % (obj.category_client.name)

    get_product.short_description = 'Product'
    get_category_client.short_description = 'Category client'
