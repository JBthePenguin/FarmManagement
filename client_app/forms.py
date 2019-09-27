from django import forms
from client_app.models import *


class CategoryForm(forms.ModelForm):
    """ form for category client """
    class Meta:
        model = CategoryClient
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nom"


class CategoryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class ClientForm(forms.ModelForm):
    """ form for client """
    category = CategoryModelChoiceField(queryset=CategoryClient.objects.all())

    class Meta:
        model = Client
        fields = ['category', 'name']

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "Catégorie"
        self.fields['name'].label = "Nom"
