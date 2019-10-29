from djmoney.models.fields import MoneyField
from django.db import models
from product_app.models import Product
from client_app.models import CategoryClient


class Price(models.Model):
    """ Model for price:
    - product: foreign key Product
    - category client: foreign key CategoryClient
    - value: Decimal (use django-money)
    unique together: product, category client"""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, db_index=True)
    category_client = models.ForeignKey(
        CategoryClient, on_delete=models.CASCADE, db_index=True)
    value = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')

    class Meta:
        unique_together = ('product', 'category_client')
