from django import forms
from client_app.models import *


class CategoryForm(forms.ModelForm):
    """ form for add or update a client's category """
    class Meta:
        model = CategoryClient
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nom"


class CategoryModelChoiceField(forms.ModelChoiceField):
    """ Model to display category's names in select category for a client"""
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class ClientForm(forms.ModelForm):
    """ form for add or update a client """
    category = CategoryModelChoiceField(
        queryset=CategoryClient.objects.all().order_by('name'))

    class Meta:
        model = Client
        fields = ['category', 'name']

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "Catégorie"
        self.fields['name'].label = "Nom"
