from django import forms
from product_app.models import Product


class ProductForm(forms.ModelForm):
    """ form for add or update a product """
    class Meta:
        model = Product
        fields = ['name', 'unit']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nom"
        self.fields['unit'].label = "Unité"
