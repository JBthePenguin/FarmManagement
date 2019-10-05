from django import forms
from basket_app.models import BasketCategory, Basket


class BasketCategoryForm(forms.ModelForm):
    """ form for category client """
    class Meta:
        model = BasketCategory
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(BasketCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nom"


class CategoryBasketModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class BasketForm(forms.ModelForm):
    """ form for basket """
    category = CategoryBasketModelChoiceField(
        queryset=BasketCategory.objects.all().order_by('name'))

    class Meta:
        model = Basket
        fields = ['category']

    def __init__(self, *args, **kwargs):
        super(BasketForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "Catégorie"
