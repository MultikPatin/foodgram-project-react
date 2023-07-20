from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Follow

from core.serializers import (
    USER_FIELDS,
    CoreUserSerializer,
    IsSubscribedMixin,
    RecipleInfoMixin
)


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


class SubscriptionsSerializer(IsSubscribedMixin, 
                              RecipleInfoMixin,
                              CoreUserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    class Meta(CoreUserSerializer.Meta): 
        fields = USER_FIELDS + [
            'is_subscribed',
            'recipes',
            'recipes_count',
        ]


class FollowerSerializer(
    # IsSubscribedMixin,
                        #  RecipleInfoMixin,
                         serializers.ModelSerializer):
    # is_subscribed = serializers.SerializerMethodField()
    # recipes = serializers.SerializerMethodField()
    # recipes_count = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    # following = GetUserSerializer()
    following = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    class Meta:
        # fields = USER_FIELDS + [
        #     'user', 
        #     'following',
        #     'is_subscribed',
        #     'recipes',
        #     'recipes_count',
        # ]
        fields = ('user', 'following')
        model = Follow
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Follow.objects.all(),
        #         fields=['user', 'following'],
        #     )
        # ]
    
    # def get_recipes_count(self, obj):
    #     return obj.recipes.all().count()
    
    # def get_recipes(self, obj):
    #     recipes_limit = int(
    #         self.context.get('recipes_limit')
    #     )
    #     resipes = Recipes.objects.values(
    #         'id',
    #         'name',
    #         'image',
    #         'cooking_time',
    #     )[:recipes_limit]
    #     return resipes 
    
    # def validate(self, data):
    #     user = data.get('user')
    #     following = data.get('following')
    #     if user == following:
    #         raise serializers.ValidationError(
    #             'На себя подписаться нельзя'
    #         )
    #     return data   
