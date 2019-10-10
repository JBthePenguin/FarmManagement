from django import forms
from django.contrib import admin
from order_app.models import *
from client_app.models import Client
from basket_app.models import Basket
from product_app.models import ProductOrdered


class ClientModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class OrderAdminForm(forms.ModelForm):
    client = ClientModelChoiceField(
        queryset=Client.objects.all().order_by('name'))

    class Meta:
        model = Order
        fields = "__all__"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    list_display = (
        'id', 'get_client', 'status',
        'creation_date', 'validation_date', 'delivery_date')

    def get_client(self, obj):
        return "%s" % (obj.client.name)

    # get_category.admin_order_field = 'category'
    get_client.short_description = 'Client'


class OrderModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.id)


class BasketModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.number)


class OrderBasketAdminForm(forms.ModelForm):
    order = OrderModelChoiceField(queryset=Order.objects.all().order_by('id'))
    basket = BasketModelChoiceField(
        queryset=Basket.objects.all().order_by('number'))

    class Meta:
        model = OrderBasket
        fields = "__all__"


@admin.register(OrderBasket)
class OrderBasketAdmin(admin.ModelAdmin):
    form = OrderBasketAdminForm
    list_display = ('id', 'get_order', 'get_basket', 'quantity_basket')

    def get_order(self, obj):
        return "%s" % (obj.order.id)

    def get_basket(self, obj):
        return "%s" % (obj.basket.number)

    # get_category.admin_order_field = 'category'
    get_order.short_description = 'Order id'
    get_basket.short_description = 'Basket number'


class BasketOrderedAdminForm(forms.ModelForm):
    order = OrderModelChoiceField(queryset=Order.objects.all())

    class Meta:
        model = BasketOrdered
        fields = "__all__"


@admin.register(BasketOrdered)
class BasketOrderedAdmin(admin.ModelAdmin):
    form = BasketOrderedAdminForm
    list_display = ('id', 'get_order', 'category_name', 'quantity')

    def get_order(self, obj):
        return "%s" % (obj.order.id)

    get_order.short_description = 'Order id'


class BasketOrderedModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.id)


class ProductOrderedModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class BasketProductOrderedAdminForm(forms.ModelForm):
    product = ProductOrderedModelChoiceField(
        queryset=ProductOrdered.objects.all().order_by('name'))
    basket = BasketOrderedModelChoiceField(
        queryset=BasketOrdered.objects.all())

    class Meta:
        model = BasketProductOrdered
        fields = "__all__"


@admin.register(BasketProductOrdered)
class BasketProductOrderedAdmin(admin.ModelAdmin):
    form = BasketProductOrderedAdminForm
    list_display = (
        'id', 'get_basket', 'get_product', 'quantity_product', 'price_product')

    def get_product(self, obj):
        return "%s" % (obj.product.name)

    def get_basket(self, obj):
        return "%s" % (obj.basket.id)

    get_product.short_description = 'Product'
    get_basket.short_description = 'Basket id'
