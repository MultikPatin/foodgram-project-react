from django.db import models

from backend.core.models import NameModel, RecipesForeign
# Create your models here.


class Ingredients(NameModel):
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=10
    )

class Tags(models.Model):
    color = models.CharField(
        verbose_name='Цвет',
        max_length=16
    )
    slug = models.SlugField(unique=True)

class Recipes(models.Model):
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientsRecipes'
    )
    tags = models.ManyToManyField(
        Tags,
        through='TagsRecipes'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
    )

class IngredientsRecipes(RecipesForeign):
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.recipes} - {self.ingredients}'
    
class TagsRecipes(RecipesForeign):
    tags = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.recipes} - {self.achievement}'
