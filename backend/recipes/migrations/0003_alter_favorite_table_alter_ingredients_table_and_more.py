# Generated by Django 4.2.3 on 2023-07-24 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='favorite',
            table='Favorite',
        ),
        migrations.AlterModelTable(
            name='ingredients',
            table='Ingredients',
        ),
        migrations.AlterModelTable(
            name='ingredientsrecipes',
            table='IngredientsRecipes',
        ),
        migrations.AlterModelTable(
            name='recipes',
            table='Recipes',
        ),
        migrations.AlterModelTable(
            name='shoppingcart',
            table='ShoppingCart',
        ),
        migrations.AlterModelTable(
            name='tags',
            table='Tags',
        ),
        migrations.AlterModelTable(
            name='tagsrecipes',
            table='TagsRecipes',
        ),
    ]
