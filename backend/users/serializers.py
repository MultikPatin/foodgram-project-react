from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import serializers

from users.models import Follow

from core.serializers import (
    USER_FIELDS,
    CoreUserSerializer,
    IsSubscribedMixin,
)

from recipes.serializers import CleanRecipeSerializer


User = get_user_model()

class PostUserSerializer(CoreUserSerializer):
    class Meta(CoreUserSerializer.Meta):
        fields = USER_FIELDS


class GetUserSerializer(IsSubscribedMixin, CoreUserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    class Meta(CoreUserSerializer.Meta):
        fields = USER_FIELDS + ['is_subscribed']


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = '__all__'


class SubscriptionsSerializer(IsSubscribedMixin, CoreUserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = CleanRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()
    class Meta(CoreUserSerializer.Meta): 
        fields = USER_FIELDS + [
            "is_subscribed",
            "recipes",
            "recipes_count",
        ]

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()
