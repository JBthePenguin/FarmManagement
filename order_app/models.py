from django.db import models
from client_app.models import Client


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, db_index=True)
    status = models.CharField(
        db_index=True, max_length=100, default="en préparation")
    creation_date = models.DateTimeField(db_index=True, auto_now_add=True)
    validation_date = models.DateTimeField(null=True, blank=True, default=None)
    delivery_date = models.DateTimeField(null=True, blank=True, default=None)
