from typing import Any
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import filters
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    SAFE_METHODS
)
from .models import (
    Ingredients,
    Tags,
    Recipes,
    Favorite,
    ShoppingCart
)
from .serializers import (
    IngredientSerializer,
    TagsSerializer,
    RecipesSerializer,
    RecipesSafeMethodSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer
)
from core.views import UserRecipesViewSet


User = get_user_model()

class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipesSafeMethodSerializer
        return RecipesSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteView(UserRecipesViewSet):
    query_set = Favorite.objects.all()
    serializer = FavoriteSerializer
    message = 'избранное'
    message_plural = 'избранном'


class ShoppingCartViewSet(UserRecipesViewSet):
    query_set = ShoppingCart.objects.all()
    serializer = ShoppingCartSerializer
    message = 'список покупок'
    message_plural = 'списке покупок'


@api_view(['GET'])
def download_shopping_cart(request):
    pass