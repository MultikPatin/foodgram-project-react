from django.contrib import admin

from .models import (
    Ingredients,
    Tags,
    Recipes,
    Favorite,
    ShoppingCart 
)

@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_editable = ('name','measurement_unit',)
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = '-пусто-'


@admin.register(Tags)
class TagssAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    list_editable = ('name','color',)
    search_fields = ('name',)
    list_filter = ('color',)
    empty_value_display = '-пусто-'
