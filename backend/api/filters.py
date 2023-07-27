import django_filters as filters

from recipes.models import Recipes, Tags



class RecipesFilter(filters.FilterSet):
    tags = filters.ModelChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tags.objects.all(),
    )

    class Meta:
        model = Recipes
        fields = ['author', 'tags']
