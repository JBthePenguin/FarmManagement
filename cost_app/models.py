from django.db import models
from djmoney.models.fields import MoneyField


class CostCategory(models.Model):
    """ Model for cost's category:
    - calcul mode: str
    - name unique: str
    unique_together: calcul_mode, name """
    calcul_mode = models.CharField(db_index=True, max_length=20)
    name = models.CharField(db_index=True, max_length=100)

    class Meta:
        unique_together = ('calcul_mode', 'name')


class Cost(models.Model):
    """ Model for cost:
    - category: foreign key CostCategory
    - name: str
    - amount: Decimal (use django-money)
    - unit used: str
    unique_together: category, name """
    category = models.ForeignKey(
        CostCategory, on_delete=models.PROTECT, db_index=True)
    name = models.CharField(db_index=True, max_length=100)
    amount = MoneyField(
        max_digits=14, decimal_places=2, default_currency='EUR')
    unit = models.CharField(max_length=20)

    class Meta:
        unique_together = ('category', 'name')


class AdditionalCost(models.Model):
    """ Model for additional cost:
    - cost: foreign key Cost
    - quantity: float
    - date added: Datetime"""
    cost = models.ForeignKey(
        Cost, on_delete=models.PROTECT, db_index=True)
    quantity = models.FloatField()
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
