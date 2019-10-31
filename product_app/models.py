from django.db import models


class Product(models.Model):
    """ Model for product:
    - product name unique: str
    - unit used: str """
    name = models.CharField(
        db_index=True, unique=True, max_length=100,
        error_messages={
            'unique': 'Un produit avec ce nom est déjà répertorié'
        }
    )
    unit = models.CharField(max_length=20)


class ProductOrdered(models.Model):
    """ Model for product ordered:
    - product name: str
    - unit used: str
    unique together """
    name = models.CharField(db_index=True, max_length=100)
    unit = models.CharField(max_length=20)

    class Meta:
        unique_together = ('name', 'unit')
