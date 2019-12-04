from django.db import models
from djmoney.models.fields import MoneyField
from client_app.models import Client
from basket_app.models import Basket
from product_app.models import Product


class Order(models.Model):
    """ Model for order:
    - client: foreign key Client
    - status : str
    - creation, validation, delivery date: datetime """
    client = models.ForeignKey(Client, on_delete=models.PROTECT, db_index=True)
    status = models.CharField(
        db_index=True, max_length=100, default="en préparation")
    creation_date = models.DateTimeField(db_index=True, auto_now_add=True)
    validation_date = models.DateTimeField(null=True, blank=True, default=None)
    delivery_date = models.DateTimeField(null=True, blank=True, default=None)


class OrderBasket(models.Model):
    """ Model for order' compositon:
    - order: foreign key Order
    - basket : foreign key Basket
    - quantity of basket : int
    unique together : order, basket """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_index=True)
    basket = models.ForeignKey(Basket, on_delete=models.PROTECT)
    quantity_basket = models.IntegerField()

    class Meta:
        unique_together = ('order', 'basket')


class BasketOrdered(models.Model):
    """ Model for basket for order validated:
    - order: foreign key Order
    - basket's category name : str
    - quantity of basket : int
    unique together : order, basket's category name """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_index=True)
    category_name = models.CharField(db_index=True, max_length=100)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('order', 'category_name')


class BasketProductOrdered(models.Model):
    """ Model for composition of basket for order validated::
    - basket: foreign key BasketOrdered
    - product: foreign key ProductOrdered
    - quantity of product: float
    - price of product : Decimal (use django-money)
    unique_together: basket, 'product """
    basket = models.ForeignKey(
        BasketOrdered, on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, db_index=True)
    quantity_product = models.FloatField()
    price_product = MoneyField(
        max_digits=14, decimal_places=2, default_currency='EUR')

    class Meta:
        unique_together = ('basket', 'product')
