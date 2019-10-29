from django import forms
from django.contrib import admin
from basket_app.models import *
from product_app.models import *


@admin.register(BasketCategory)
class BasketCategoryAdmin(admin.ModelAdmin):
    """ Model for basket's category in admin site """
    list_display = ('id', 'name')


class CategoryBasketModelChoiceField(forms.ModelChoiceField):
    """ Model to display category's names in select category
    for save a basket in admin site"""
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class BasketAdminForm(forms.ModelForm):
    """ Form to save a basket in admin site"""
    category = CategoryBasketModelChoiceField(
        queryset=BasketCategory.objects.all())

    class Meta:
        model = Basket
        fields = "__all__"


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    """ Model for basket in admin site """
    form = BasketAdminForm
    list_display = ('id', 'number', 'get_category')

    def get_category(self, obj):
        """ return the name of the category for basket's table in admin site"""
        return "%s" % (obj.category.name)

    get_category.short_description = 'Category'


class BasketModelChoiceField(forms.ModelChoiceField):
    """ Model to display basket number in select basket
    for save a composition in admin site"""
    def label_from_instance(self, obj):
        return "%s" % (obj.number)


class ProductModelChoiceField(forms.ModelChoiceField):
    """ Model to display product name in select product
    for save a composition in admin site"""
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class BasketProductAdminForm(forms.ModelForm):
    """ Form to save a composition in admin site"""
    product = ProductModelChoiceField(
        queryset=Product.objects.all())
    basket = BasketModelChoiceField(
        queryset=Basket.objects.all())

    class Meta:
        model = BasketProduct
        fields = "__all__"


@admin.register(BasketProduct)
class BasketProductAdmin(admin.ModelAdmin):
    """ Model for composition in admin site """
    form = BasketProductAdminForm
    list_display = ('id', 'get_basket', 'get_product', 'quantity_product')

    def get_product(self, obj):
        """ return the name of the product
        for composition's table in admin site"""
        return "%s" % (obj.product.name)

    def get_basket(self, obj):
        """ return the number of the basket
        for composition's table in admin site"""
        return "%s" % (obj.basket.number)

    get_product.short_description = 'Product'
    get_basket.short_description = 'Basket number'
