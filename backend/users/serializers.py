from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Follow

from core.serializers import (
    CoreUserSerializer,
    IsSubscribedMixin,
    RecipleInfoMixin
)


User = get_user_model()

USER_FIELDS = [
    'email',
    'id',
    'username',
    'first_name',
    'last_name',
]

class PostUserSerializer(CoreUserSerializer):
    class Meta(CoreUserSerializer.Meta):
        fields = USER_FIELDS


class GetUserSerializer(IsSubscribedMixin):
    class Meta(CoreUserSerializer.Meta):
        fields = USER_FIELDS + ['is_subscribed']


class PasswordSerializer(CoreUserSerializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'


class SubscriptionsSerializer(IsSubscribedMixin,
                              RecipleInfoMixin,):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    class Meta(CoreUserSerializer.Meta): 
        fields = USER_FIELDS + [
            'is_subscribed',
            'recipes',
            'recipes_count',
        ]


class FollowerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    following = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
            )
        ]
    
    def validate(self, data):
        user = data.get('user')
        following = data.get('following')
        if user == following:
            raise serializers.ValidationError(
                'На себя подписаться нельзя'
            )
        return data   
