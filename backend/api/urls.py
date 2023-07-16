from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from recipes.views import (
    RecipesViewSet,
    TagsViewSet,
    IngredientsViewSet
)

from users.views import (
    CustomUserViewSet  
)

router = DefaultRouter()

router.register("recipes",
                RecipesViewSet,
                basename="recipes")
router.register("tags",
                TagsViewSet,
                basename="tags")
router.register("ingredients",
                IngredientsViewSet,
                basename="ingredients")
router.register("users",
                CustomUserViewSet,
                basename="recipes")

urlpatterns = [
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include('djoser.urls')),    
]
