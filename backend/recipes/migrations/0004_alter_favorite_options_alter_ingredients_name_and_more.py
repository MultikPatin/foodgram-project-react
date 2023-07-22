# Generated by Django 4.2.3 on 2023-07-21 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_favorite'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'ordering': ['user'], 'verbose_name': 'избранное', 'verbose_name_plural': 'рецепты -> избранное'},
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='name',
            field=models.CharField(help_text='Введите название', max_length=200, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='name',
            field=models.CharField(help_text='Введите название', max_length=200, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(help_text='Введите название', max_length=200, verbose_name='название'),
        ),
    ]