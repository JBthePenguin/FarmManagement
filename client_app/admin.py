from django import forms
from django.contrib import admin
from client_app.models import *


@admin.register(CategoryClient)
class CategoryClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class CategoryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class ClientAdminForm(forms.ModelForm):
    category = CategoryModelChoiceField(queryset=CategoryClient.objects.all())

    class Meta:
        model = Client
        fields = "__all__"


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    form = ClientAdminForm
    list_display = ('id', 'get_category', 'name')

    def get_category(self, obj):
        return "%s" % (obj.category.name)

    # get_category.admin_order_field = 'category'
    get_category.short_description = 'Category'
