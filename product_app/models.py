from django.db import models


class Product(models.Model):
    name = models.CharField(db_index=True, unique=True, max_length=100)
    unit = models.CharField(max_length=20)
