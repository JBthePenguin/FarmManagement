from django import forms
from django.contrib import admin
from price_app.models import Price
from product_app.models import Product
from client_app.models import CategoryClient


class ProductModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class CategoryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class PriceAdminForm(forms.ModelForm):
    product = CategoryModelChoiceField(
        queryset=Product.objects.all())
    category_client = CategoryModelChoiceField(
        queryset=CategoryClient.objects.all())

    class Meta:
        model = Price
        fields = "__all__"


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    form = PriceAdminForm
    list_display = ('get_product', 'get_category_client', 'value')

    def get_product(self, obj):
        return "%s" % (obj.product.name)

    def get_category_client(self, obj):
        return "%s" % (obj.category_client.name)

    get_product.short_description = 'Product'
    get_category_client.short_description = 'Category client'
