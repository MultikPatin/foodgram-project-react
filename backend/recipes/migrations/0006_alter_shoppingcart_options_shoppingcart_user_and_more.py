# Generated by Django 4.2.3 on 2023-07-22 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0005_alter_ingredients_name_alter_recipes_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'ordering': ['user'], 'verbose_name': 'избранное', 'verbose_name_plural': 'рецепты -> избранное'},
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(default=1, help_text='Выберите пользователя', on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipes',
            field=models.ForeignKey(help_text='Выберите рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='shoppingcart', to='recipes.recipes', verbose_name='рецепт'),
        ),
    ]
