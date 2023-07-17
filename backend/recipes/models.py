from django.contrib.auth import get_user_model
from django.db import models

from core.models import (
    NameMixinModel,
    AuthorMixinModel,
)

User = get_user_model()

class Ingredients(NameMixinModel):
    
    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=10,
        help_text='Введите единицу измерения'
    )


class Tags(NameMixinModel):
    
    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'теги'

    color = models.CharField(
        'Цвет',
        max_length=16,
        help_text='Введите цвет'
    )
    slug = models.SlugField(unique=True)


class Recipes(NameMixinModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientsRecipes',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tags,
        through='TagsRecipes',
        related_name='recipes'
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


class IngredientsRecipes(models.Model):
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='ingredientsrecipes'
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='ingredientsrecipes'
    )
    amount = models.IntegerField(
        verbose_name='Количество',
    )


class TagsRecipes(models.Model):
    tags = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE
    )

# 
# 
# 
# 

class Favorite(AuthorMixinModel):

    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorite'
    )


class ShoppingCart(models.Model):

    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='shoppingcart'
    )
