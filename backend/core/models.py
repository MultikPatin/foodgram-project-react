from django.db import models

from backend.recipes.models import Recipes

class NameModel(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True
    )

    def __str__(self):
        return self.name

class RecipesForeign(models.Model):
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE
    )