import base64
import logging

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer

from recipes.models import (
    Ingredients,
    Tags,
    Recipes,
    IngredientsRecipes,
    TagsRecipes,
    Favorite,
    ShoppingCart,
)

logger = logging.getLogger(__name__)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredients
        fields = '__all__'
        read_only_fields = ['name', 'measurement_unit']


class TagsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tags
        fields = '__all__'
        read_only_fields = ['name', 'color', 'slug']
        

class RecipeSafeMethodSerializer(WritableNestedModelSerializer):
    
    class Meta:
        model = Recipes
        fields = '__all__'
        
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    ingredients = IngredientsSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True,
    )
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    
    # def get_ingredients(self, obj):
    #     return obj.ingredients.values(
    #         'id',
    #         'name',
    #         'measurement_unit',
    #         amount=F('ingredientrecipe__amount')
    #     )

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=self.context['request'].user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=self.context['request'].user, recipe=obj
        ).exists


# class RecipeSafeMethodSerializer(serializers.ModelSerializer):
#     tags = TagSerializer(many=True, required=False)
#     author = CustomDjoserUserSerializer(
#         read_only=True, default=serializers.CurrentUserDefault()
#     )
#     ingredients = serializers.SerializerMethodField()
#     image = Base64ImageField()
#     is_favorited = serializers.SerializerMethodField()
#     is_in_shopping_cart = serializers.SerializerMethodField()

#     def get_ingredients(self, obj):
#         return obj.ingredients.values(
#             'id',
#             'name',
#             'measurement_unit',
#             amount=F('ingredientrecipe__amount')
#         )

#     def get_is_favorited(self, obj):
#         if self.context['request'].user.is_anonymous:
#             return False
#         return Favorite.objects.filter(
#             user=self.context['request'].user, recipe=obj
#         ).exists()

#     def get_is_in_shopping_cart(self, obj):
#         if self.context['request'].user.is_anonymous:
#             return False
#         return ShoppingCart.objects.filter(
#             user=self.context['request'].user, recipe=obj
#         ).exists

#     class Meta:
#         model = Recipe
#         exclude = ('pub_date',)


# class RecipeSerializer(RecipeSafeMethodSerializer):
#     ingredients = IngredinetsRecipeSerializer(many=True)
#     tags = serializers.PrimaryKeyRelatedField(
#         queryset=Tag.objects.all(), many=True
#     )
#     is_favorited = None
#     is_in_shopping_cart = None

#     def create(self, validated_data):
#         tags = validated_data.pop('tags')
#         ingredients = validated_data.pop('ingredients')
#         recipe = Recipe.objects.create(**validated_data)
#         recipe.tags.set(tags)
#         for ingredient in ingredients:
#             IngredientRecipe.objects.create(
#                 ingredient=Ingredient.objects.filter(
#                     id=ingredient['id']
#                 ).first(),
#                 recipe=recipe,
#                 amount=ingredient['amount']
#             )
#         return recipe

#     def update(self, instance, validated_data):
#         tags = validated_data.pop('tags')
#         ingredients = validated_data.pop('ingredients')
#         instance.tags.clear()
#         return super().update(instance, validated_data)

#     def to_representation(self, instance):
#         print(instance.name)
#         return RecipeSafeMethodSerializer(
#             instance, context={'request': self.context.get('request')}
#         ).data
        
#     def get_is_in_shopping_cart(self, obj):
#         if self.context['request'].user.is_anonymous:
#             return False
#         return ShoppingCart.objects.filter(
#             user=self.context['request'].user, recipe=obj
#         ).exists