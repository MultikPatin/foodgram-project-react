from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import filters
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from recipes.models import (
    Ingredients,
    Tags,
    Recipes
)
from api.serializers import (
    IngredientsSerializer,
    TagsSerializer,
    RecipesSerializer,
)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']

class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    
    def perform_create(self, serializer: RecipesSerializer):
        serializer.save(author=self.request.user)


