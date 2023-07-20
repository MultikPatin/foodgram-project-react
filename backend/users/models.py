from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Meta:
        ordering = ['id']
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='email',
        help_text='Введите email'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='логин',
        help_text='Введите логин'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='имя пользователя',
        help_text='Введите имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия пользователя',
        help_text='Введите фамилию'
    )

    USERNAME_FIELDS = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return str(self.username)


class Follow(models.Model):

    class Meta:
        ordering = ['user']
        verbose_name = 'подписку'
        verbose_name_plural = 'пользователь -> подписки'
        unique_together = ('user', 'following')

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор',
        help_text='Выберите автора'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='подписчик',
        help_text='Выберите подписчика'
    )


class Favorite(models.Model):
    
    class Meta:
        ordering = ['user']
        verbose_name = 'избранное'
        verbose_name_plural = 'пользователь -> избранное'
    
    recipes = models.ForeignKey(
        to='recipes.Recipes',
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='рецепт',
        help_text='Выберите рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='пользователь',
        help_text='Выберите пользователя'
    )
