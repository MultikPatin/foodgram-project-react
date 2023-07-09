# Generated by Django 4.2.3 on 2023-07-09 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipes',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipes',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.IngredientsRecipes', to='recipes.ingredients'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', through='recipes.TagsRecipes', to='recipes.tags'),
        ),
    ]
