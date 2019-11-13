from django import forms
from cost_app.models import CostCategory, Cost


class CostCategoryForm(forms.ModelForm):
    """ form for add or update a cost's category """
    class Meta:
        model = CostCategory
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(CostCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nom"


class CostForm(forms.ModelForm):
    """ form for add a cost """
    class Meta:
        model = Cost
        fields = ['name', 'amount', 'unit']

    def __init__(self, *args, **kwargs):
        super(CostForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nom"
        self.fields['amount'].label = "Montant"
        self.fields['unit'].label = "Unité"


class CostCategoryModelChoiceField(forms.ModelChoiceField):
    """ Model to display category's names in select category for a cost"""
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class CostUpdateForm(forms.ModelForm):
    """ form for update a cost """
    category = CostCategoryModelChoiceField(
        queryset=CostCategory.objects.all().order_by('name'))

    class Meta:
        model = Cost
        fields = ['category', 'name', 'amount', 'unit']

    def __init__(self, *args, **kwargs):
        super(CostUpdateForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "Catégorie"
        self.fields['name'].label = "Nom"
        self.fields['amount'].label = "Montant"
        self.fields['unit'].label = "Unité"
