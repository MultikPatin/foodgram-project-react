from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from api.views import (
    TagsViewSet,
    IngredientsViewSet,
    RecipesViewSet,
    SubscribeViewSet,
)


app_name = "api"

router = DefaultRouter()

router.register(
    r"users/(?P<author_id>\d+)/subscribe",
    SubscribeViewSet,
    basename="subscribe",
)
# router.register("subscribe", SubscribeViewSet, basename="subscribe")
router.register("recipes", RecipesViewSet, basename="recipes")
router.register("tags", TagsViewSet, basename="tags")
router.register("ingredients", IngredientsViewSet, basename="ingredients")

# router.register(
#     r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
#     CommentViewSet,
#     basename="comments",
# )

urlpatterns = [
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include('djoser.urls')),    
]
