from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import serializers

from users.models import Follow


User = get_user_model()

class GetUserSerializer(serializers.ModelSerializer):
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


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  ]


class SubscribeSerializer(serializers.ModelSerializer):
    pass