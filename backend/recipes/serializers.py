from django.contrib.auth import get_user_model

from rest_framework import serializers

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
        

class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='ingredients.id',
    )
    name = serializers.CharField(
        source='ingredients.name',
    )
    measurement_unit = serializers.CharField(
        source='ingredients.measurement_unit',
    )

    class Meta:
        model = IngredientsRecipes
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientsRecipesSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all()
    )
    class Meta:
        model = IngredientsRecipes
        fields = ('id', 'amount',)


class TagsSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Tags
        fields = '__all__'
        read_only_fields = ['name', 'color', 'slug']
        

class RecipesSafeMethodSerializer(IsFavoriteOrShopingCardMixin):
    author = GetUserSerializer(read_only=True)
    tags = TagsSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    class Meta(CoreRecipeSerializer.Meta):
        fields = '__all__'
    
    def get_ingredients(self, obj):
        ingredients = IngredientsRecipes.objects.filter(recipes=obj)
        return IngredientInRecipeSerializer(
            ingredients,
            many=True
        ).data


class RecipesSerializer(IsFavoriteOrShopingCardMixin):
    author = GetUserSerializer(read_only=True)
    ingredients = IngredientsRecipesSerializer(many=True)
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tags.objects.all(),
        slug_field='id'
    )
    cooking_time = serializers.IntegerField()
    class Meta(CoreRecipeSerializer.Meta):
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        ]

    def validate_cooking_time(self, data):
        if data <= 0:
            raise serializers.ValidationError('Введите число больше 0')
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipes.objects.create(
            author=author,
            **validated_data
        )
        for ingredient in ingredients:
            ingredient_model = ingredient['id']
            amount = ingredient['amount']
            IngredientsRecipes.objects.create(
                ingredients=ingredient_model,
                recipes=recipe,
                amount=amount
            )
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        tags_data = validated_data.pop("tags")
        TagsRecipes.objects.filter(recipes=instance).delete()
        IngredientsRecipes.objects.filter(recipes=instance).delete()
        for ingredient in ingredients_data:
            ingredient_model = ingredient["id"]
            amount = ingredient["amount"]
            IngredientsRecipes.objects.create(
                ingredients=ingredient_model,
                recipes=instance,
                amount=amount
            )
        instance.name = validated_data.pop("name")
        instance.text = validated_data.pop("text")
        if validated_data.get("image") is not None:
            instance.image = validated_data.pop("image")
        instance.cooking_time = validated_data.pop("cooking_time")
        instance.tags.set(tags_data)
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipesSafeMethodSerializer(
            instance,
            context={
                'request': self.context.get('request')}
        ).data


class FavoriteSerializer(UserRecipesSerializer):
    class Meta(UserRecipesSerializer.Meta):
        model = Favorite


class ShoppingCartSerializer(UserRecipesSerializer):
    class Meta(UserRecipesSerializer.Meta):
        model = ShoppingCart