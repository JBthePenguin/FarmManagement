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
