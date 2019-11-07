from django import forms
from cost_app.models import CostCategory


class CostCategoryForm(forms.ModelForm):
    """ form for add or update a cost's category """
    class Meta:
        model = CostCategory
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(CostCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nom"
