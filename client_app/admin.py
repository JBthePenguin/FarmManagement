from django import forms
from django.contrib import admin
from client_app.models import *


@admin.register(CategoryClient)
class CategoryClientAdmin(admin.ModelAdmin):
    """ Model for client's category in admin site """
    list_display = ('id', 'name')


class CategoryModelChoiceField(forms.ModelChoiceField):
    """ Model to display category's names in select category
    for save a client in admin site"""
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class ClientAdminForm(forms.ModelForm):
    """ Form to save a client in admin site"""
    category = CategoryModelChoiceField(queryset=CategoryClient.objects.all())

    class Meta:
        model = Client
        fields = "__all__"


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """ Model for client in admin site """
    form = ClientAdminForm
    list_display = ('id', 'get_category', 'name')

    def get_category(self, obj):
        """ return the name of the category for client's table in admin site"""
        return "%s" % (obj.category.name)

    # get_category.admin_order_field = 'category'
    get_category.short_description = 'Category'
