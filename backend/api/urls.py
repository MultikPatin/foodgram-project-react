from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from recipes.views import (
    RecipesViewSet,
    TagsViewSet,
    IngredientsViewSet,
    FavoriteView,
    ShoppingCartViewSet,
    download_shopping_cart
)

from users.views import (
    CustomUserViewSet,
)

router = DefaultRouter()
router.register('recipes',
                RecipesViewSet,
                basename='recipes')
    #/recipes/                  [get, post]
    #/recipes/{id}/             [get, patch, delete]
router.register('tags',
                TagsViewSet,
                basename='tags')
    #/tags/                     [get]
    #/tags/{id}/                [get]
router.register('ingredients',
                IngredientsViewSet,
                basename='ingredients')
    #/ingredients/              [get]
    #/ingredients/{id}/         [get]
router.register('users',
                CustomUserViewSet,
                basename='recipes')
    #/users/                    [get, post]
    #/users/{id}/               [get]
    #/users/me/                 [get]
    #/users/set_password/       [post]
urlpatterns = [
    re_path(r'^auth/', include('djoser.urls.authtoken')),
                    # /token/login/                     [post]
                    # /token/logout/                    [post]
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download',
    ),
                    #/recipes/download_shopping_cart/   [get]
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteView.as_view(),
    ),
                    # /recipes/{id}/favorite/           [post, delete]
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        ShoppingCartViewSet.as_view(),
    ),
                    # /recipes/{id}/shopping_cart/      [post, delete]
    path('', include(router.urls)),
]
