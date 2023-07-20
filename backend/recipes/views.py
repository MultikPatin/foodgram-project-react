from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import filters
from rest_framework import status, viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    SAFE_METHODS
)
from .models import (
    Ingredients,
    Tags,
    Recipes
)
from .serializers import (
    IngredientsSerializer,
    TagsSerializer,
    RecipesSerializer,
    RecipesSafeMethodSerializer,
)


User = get_user_model()

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
    
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipesSafeMethodSerializer
        return RecipesSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



