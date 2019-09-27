from django.db import models


class CategoryClient(models.Model):
    name = models.CharField(
        db_index=True, unique=True, max_length=100,
        error_messages={
            'unique': 'Une catégorie avec ce nom est déjà répertoriée'
        }
    )


class Client(models.Model):
    category = models.ForeignKey(
        CategoryClient, on_delete=models.PROTECT, db_index=True)
    name = models.CharField(
        db_index=True, unique=True, max_length=100,
        error_messages={
            'unique': 'Un client avec ce nom est déjà répertorié'
        }
    )
