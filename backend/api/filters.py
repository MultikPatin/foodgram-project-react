import django_filters as filters

from recipes.models import Recipes, Tags, Ingredients


class RecipesFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tags.objects.all(),
    )

    class Meta:
        model = Recipes
        fields = ['author', 'tags']


class IngredientsFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='startswith'
    )

    class Meta:
        model = Ingredients
        fields = ['name']
