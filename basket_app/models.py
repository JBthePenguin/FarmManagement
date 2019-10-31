from django.db import models
from product_app.models import *


class BasketCategory(models.Model):
    """ Model for basket's category:
    - name unique: str """
    name = models.CharField(
        db_index=True, unique=True, max_length=100,
        error_messages={
            'unique': 'Une catégorie avec ce nom est déjà répertoriée'
        }
    )


class Basket(models.Model):
    """ Model for client's category:
    - number unique (like an indice): int
    - category: foreign key BasketCategory """
    number = models.IntegerField(
        db_index=True, unique=True,
        error_messages={
            'unique': 'Un panier avec ce numéro est déjà répertorié'
        }
    )
    category = models.ForeignKey(
        BasketCategory, on_delete=models.PROTECT, db_index=True)


class BasketProduct(models.Model):
    """ Model for basket's composition:
    - basket: foreign key Basket
    - product: foreign key Product
    - quantity of product: float
    unique_together: basket, 'product """
    basket = models.ForeignKey(
        Basket, on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, db_index=True)
    quantity_product = models.FloatField()

    class Meta:
        unique_together = ('basket', 'product')
