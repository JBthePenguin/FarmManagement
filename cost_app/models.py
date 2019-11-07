from django.db import models


class CostCategory(models.Model):
    """ Model for cost's category:
    - calcul mode: str
    - name unique: str
    unique_together: calcul_mode, name """
    calcul_mode = models.CharField(db_index=True, max_length=20)
    name = models.CharField(db_index=True, max_length=100)

    class Meta:
        unique_together = ('calcul_mode', 'name')
