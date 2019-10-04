from django import forms
from basket_app.models import BasketCategory


class BasketCategoryForm(forms.ModelForm):
    """ form for category client """
    class Meta:
        model = BasketCategory
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(BasketCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nom"
