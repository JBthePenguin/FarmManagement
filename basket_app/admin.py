from django import forms
from django.contrib import admin
from basket_app.models import *
from product_app.models import Product


@admin.register(BasketCategory)
class BasketCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class CategoryBasketModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class BasketAdminForm(forms.ModelForm):
    category = CategoryBasketModelChoiceField(
        queryset=BasketCategory.objects.all())

    class Meta:
        model = Basket
        fields = "__all__"


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    form = BasketAdminForm
    list_display = ('id', 'number', 'get_category')

    def get_category(self, obj):
        return "%s" % (obj.category.name)

    get_category.short_description = 'Category'


class BasketModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.number)


class ProductModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class BasketProductAdminForm(forms.ModelForm):
    product = ProductModelChoiceField(
        queryset=Product.objects.all())
    basket = BasketModelChoiceField(
        queryset=Basket.objects.all())

    class Meta:
        model = BasketProduct
        fields = "__all__"


@admin.register(BasketProduct)
class BasketProductAdmin(admin.ModelAdmin):
    form = BasketProductAdminForm
    list_display = ('id', 'get_basket', 'get_product', 'quantity_product')

    def get_product(self, obj):
        return "%s" % (obj.product.name)

    def get_basket(self, obj):
        return "%s" % (obj.basket.number)

    get_product.short_description = 'Product'
    get_basket.short_description = 'Basket number'
