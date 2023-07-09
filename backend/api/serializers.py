import base64

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
)


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


class RecipesSerializer(WritableNestedModelSerializer):
    
    class Meta:
        model = Recipes
        fields = '__all__'
        
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    ingredients = IngredientsSerializer(many=True)
    tags = serializers.SlugRelatedField(
        slug_field='id', 
        queryset=Tags.objects.all(),
        many=True
    )
    image = Base64ImageField(required=False, allow_null=True)
