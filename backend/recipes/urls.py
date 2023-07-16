from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from api.views import (
    TagsViewSet,
    IngredientsViewSet,
    RecipesViewSet,
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

urlpatterns = [
    path('', include(router.urls)),  
]
