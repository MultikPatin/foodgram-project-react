# Generated by Django 4.2.3 on 2023-07-21 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_favorite_options_alter_favorite_recipes_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]