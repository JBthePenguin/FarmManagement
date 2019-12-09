from django import template
from client_app.models import Client

register = template.Library()


@register.filter
def get_clients(category):
    """ return all clients for a specific client's category """
    return Client.objects.filter(category=category).order_by('name')
