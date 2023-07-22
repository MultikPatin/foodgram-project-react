from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import serializers

# from drf_extra_fields.fields import Base64ImageField

from recipes.models import (
    Ingredients,
    Tags,
    Recipes,
    IngredientsRecipes,
    TagsRecipes,
    Favorite,
    ShoppingCart,   
)
from users.serializers import GetUserSerializer

from core.serializers import (
    CoreRecipeSerializer,
    UserRecipesSerializer
)

from core.serializers import (
    IsFavoriteOrShopingCardMixin
)


User = get_user_model()
        
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'
        read_only_fields = ['name', 'measurement_unit']


class IngredientsRecipesSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all(),
    )
    class Meta:
        model = IngredientsRecipes
        fields = ('id', 'amount')


class TagsSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Tags
        fields = '__all__'
        read_only_fields = ['name', 'color', 'slug']
        

class RecipesSafeMethodSerializer(IsFavoriteOrShopingCardMixin):
    author = GetUserSerializer()
    tags = TagsSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
    class Meta(CoreRecipeSerializer.Meta):
        fields = '__all__'
    
    def get_ingredients(self, obj):
        ingredients = IngredientsRecipes.objects.filter(
            recipes=obj.id
        ).values()
        return ingredients


class RecipesSerializer(IsFavoriteOrShopingCardMixin):
    ingredients = IngredientsRecipesSerializer(many=True)
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tags.objects.all(),
        slug_field='id'
    )
    class Meta(CoreRecipeSerializer.Meta):
        fields = [
            'ingredients',
            'tags',
            'image',
            'text',
            'name',
            'cooking_time'
        ]

    def validate_cooking_time(self, data):
        if data <= 0:
            raise serializers.ValidationError("Введите число больше 0")
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(**validated_data)
        recipe.tags.set(tags)
        for item in ingredients:
            ingredients = Ingredients.objects.filter(
                    name=item['id']
                )
            amount = item['amount']
            IngredientsRecipes.objects.create(
                ingredients=ingredients,
                recipes=recipe,
                amount=amount
            )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.clear()
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        print(instance.name)
        return RecipesSafeMethodSerializer(
            instance, context={'request': self.context.get('request')}
        ).data


class FavoriteSerializer(UserRecipesSerializer):
    class Meta(UserRecipesSerializer.Meta):
        model = Favorite


class ShoppingCartSerializer(UserRecipesSerializer):
    class Meta(UserRecipesSerializer.Meta):
        model = ShoppingCart