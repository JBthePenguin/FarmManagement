from django import forms
from client_app.models import *


class CategoryForm(forms.ModelForm):
    """ form for product """
    class Meta:
        model = CategoryClient
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nom"
