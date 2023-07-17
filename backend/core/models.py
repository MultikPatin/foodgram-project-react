from django.contrib.auth import get_user_model
from django.db import models

# from recipes.models import Recipes


User = get_user_model()

class NameMixinModel(models.Model):
    
    class Meta:
        abstract = True
        
    name = models.CharField(
        'название',
        max_length=200,
        unique=True,
        help_text='Введите название'
    )

    def __str__(self):
        return self.name

class AuthorMixinModel(models.Model):
    
    class Meta:
        abstract = True
        
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )

# class RecipesMixinModel(models.Model):
    
#     class Meta:
#         abstract = True
        
#     author = models.ForeignKey(
#         Recipes,
#         on_delete=models.CASCADE,
#         related_name='recipes'
#     )