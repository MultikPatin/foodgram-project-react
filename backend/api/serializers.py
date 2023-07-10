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
    Follow
)
from users.models import User

logger = logging.getLogger(__name__)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed'
                  ]

    is_subscribed = serializers.SerializerMethodField()
    
    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=self.context['request'].user, 
            author=obj.id
        ).exists()
    
    
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
        

class RecipeSafeMethodSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Recipes
        fields = '__all__'

    tags = TagsSerializer(many=True)
    author = UserSerializer()
    
    ingredients = serializers.SerializerMethodField()
    
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)
    
    
    def get_ingredients(self, obj):
        # res = obj.ingredients.values(
        #     'id',
        #     'name',
        #     'measurement_unit',
        #     # amount='ingredientsrecipes__amount'
        # )
        amount_list = IngredientsRecipes.objects.filter(
            recipes=obj.id
        ).values()
        return amount_list

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Favorite.objects.filter(
            author=self.context['request'].user, 
            recipes=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            author=self.context['request'].user, 
            recipes=obj.id
        ).exists()



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