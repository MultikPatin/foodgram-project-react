from django.db import models

from users.models import User


class Ingredients(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=10
    )
    
    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=16
    )
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True
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
    
    def __str__(self):
        return self.name


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
        default=0
    )

    def __str__(self):
        return f'{self.recipes} <-> {self.ingredients}'

  
class TagsRecipes(models.Model):
    tags = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.recipes} <-> {self.tags}'


class Favorite(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorite'
    )


class ShoppingCart(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcart'
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='shoppingcart'
    )
