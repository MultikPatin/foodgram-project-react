from django.contrib.auth import get_user_model

from rest_framework import filters
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticatedOrReadOnly,
)
from .models import (
    Ingredients,
    Tags,
    Recipes,
    Favorite,
    ShoppingCart,
    IngredientsRecipes,  
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

from api.permissions import AuthorOrReadOnly


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
    permission_classes = [AuthorOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipesSafeMethodSerializer
        return RecipesSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            'Рецепт успешно удален',
            status=status.HTTP_204_NO_CONTENT
        )


class FavoriteView(UserRecipesViewSet):
    queryset = Favorite.objects.all()
    serializer = FavoriteSerializer
    message = 'избранное'
    message_plural = 'избранном'


class ShoppingCartViewSet(UserRecipesViewSet):
    queryset = ShoppingCart.objects.all()
    serializer = ShoppingCartSerializer
    message = 'список покупок'
    message_plural = 'списке покупок'


@api_view(['GET'])
def download_shopping_cart(request):
    user = request.user
    shopping_cart = ShoppingCart.objects.filter(
        user=user
    )

    buying_list = {}
    for record in shopping_cart:
        recipe = record.recipes
        ingredients = IngredientsRecipes.objects.filter(
            recipes=recipe
        )
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredients.name
            measurement_unit = ingredient.ingredients.measurement_unit
            if name not in buying_list:
                buying_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount,
                }
            else:
                buying_list[name]['amount'] = (
                    buying_list[name]['amount'] + amount
                )

    shopping_list = []
    for name, data in buying_list.items():
        amount = data['amount']
        measurement_unit = data['measurement_unit']
        shopping_list.append(
            f'{name} - {amount} {measurement_unit}'
        )
    print(shopping_list)
    return Response(
            shopping_list,
            status=status.HTTP_201_CREATED
        )
