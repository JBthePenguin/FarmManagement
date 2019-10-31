from django import forms
from order_app.models import Order
from client_app.models import Client


class ClientModelChoiceField(forms.ModelChoiceField):
    """ Model to display client's names in select client for an order"""
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class OrderForm(forms.ModelForm):
    """ form for create or update an order """
    client = ClientModelChoiceField(
        queryset=Client.objects.all().order_by('name'))

    class Meta:
        model = Order
        fields = ['client']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['client'].label = "Client"
