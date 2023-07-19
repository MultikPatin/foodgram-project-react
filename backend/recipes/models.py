from django.contrib.auth import get_user_model
from django.db import models

from core.models import (
    NameMixinModel,
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
    
    class Meta:
        ordering = ['id']
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор',
        help_text='Выберите автора'
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
        default=None,
        verbose_name='Изображение',
        help_text='Выберите изображение'
    )
    text = models.TextField(
        verbose_name='описание',
        help_text='Введите описание'
    )
    cooking_time = models.IntegerField(
        verbose_name='время приготовления',
        help_text='Введите время приготовления в минутах'
    )


class IngredientsRecipes(models.Model):
    
    class Meta:
        ordering = ['recipes']
        verbose_name = 'строки ингредиентов к рецептам'
        verbose_name_plural = 'рецепты -> ингредиенты'

    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='ingredientsrecipes',
        verbose_name='ингредиент',
        help_text='Выберите ингредиент'
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='ingredientsrecipes',
        verbose_name='рецепт',
        help_text='Выберите рецепт'
    )
    amount = models.IntegerField(
        verbose_name='количество',
        help_text='Введите количество'
    )


class TagsRecipes(models.Model):
    
    class Meta:
        ordering = ['recipes']
        verbose_name = 'строки тегов к рецептам'
        verbose_name_plural = 'рецепты -> теги'

    tags = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        related_name='tagsrecipes',
        verbose_name='тег',
        help_text='Выберите тег'
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='tagsrecipes',
        verbose_name='рецепт',
        help_text='Выберите рецепт'
    )

# 
# 
# 
# 



class ShoppingCart(models.Model):

    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='shoppingcart'
    )
