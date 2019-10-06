from django import forms
from django.contrib import admin
from order_app.models import *
from client_app.models import Client


class ClientModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class OrderAdminForm(forms.ModelForm):
    client = ClientModelChoiceField(queryset=Client.objects.all())

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
