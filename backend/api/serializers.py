from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import (
    Ingredients,
    Tags,
    Recipes,
)


class IngredientsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredients
        fields = '__all__'
 
class TagsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tags
        fields = '__all__'

class RecipesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Recipes
        fields = '__all__'
        
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    ingredients = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Ingredients.objects.all()
    )
    tags = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Tags.objects.all()
    )
    
    # def validate(self, data):
    #     request = self.context["request"]
    #     if request.method == "POST":
    #         author = request.user
    #         title_id = self.context.get("view").kwargs.get("title_id")
    #         title = get_object_or_404(Title, pk=title_id)
    #         if Review.objects.filter(title=title, author=author).exists():
    #             raise ValidationError("Может существовать только один отзыв!")
    #     return data