from django.contrib.auth import get_user_model

from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from users.models import Follow

from recipes.models import (
    Recipes,
    Favorite,
    ShoppingCart
)


User = get_user_model()


class CoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class IsSubscribedMixin(CoreUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user,
            following=obj
        ).exists()


class UserRecipesSerializer(serializers.ModelSerializer):
    recipes = serializers.PrimaryKeyRelatedField(
        queryset=Recipes.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        fields = '__all__'


class CoreRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipes


class IsFavoriteOrShopingCardMixin(CoreRecipeSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user,
            recipes=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user,
            recipes=obj
        ).exists()
