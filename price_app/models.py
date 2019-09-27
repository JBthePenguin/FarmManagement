from djmoney.models.fields import MoneyField
from django.db import models
from product_app.models import Product
from client_app.models import CategoryClient


class Price(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, db_index=True)
    category_client = models.ForeignKey(
        CategoryClient, on_delete=models.CASCADE, db_index=True)
    value = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
