# Generated by Django 4.2.3 on 2023-07-09 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_recipes_author_alter_recipes_ingredients_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientsrecipes',
            name='amount',
            field=models.IntegerField(default=1, verbose_name='Количество'),
            preserve_default=False,
        ),
    ]