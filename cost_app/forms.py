from django import forms
from cost_app.models import CostCategory, Cost, AdditionalCost
from django.core.exceptions import NON_FIELD_ERRORS


class CostCategoryForm(forms.ModelForm):
    """ form for add or update a cost's category """
    class Meta:
        model = CostCategory
        fields = ['calcul_mode', 'name']
        widgets = {'calcul_mode': forms.HiddenInput()}
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Une catégorie avec ce nom est déjà répertoriée",
            }
        }

    def __init__(self, *args, **kwargs):
        super(CostCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nom"


class CostForm(forms.ModelForm):
    """ form for add a cost """
    class Meta:
        model = Cost
        fields = ['category', 'name', 'amount', 'unit']
        widgets = {'category': forms.HiddenInput()}
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Un coût avec ce nom est déjà répertorié",
            }
        }

    def __init__(self, *args, **kwargs):
        super(CostForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nom"
        self.fields['amount'].label = "Montant"
        self.fields['unit'].label = "Unité"
