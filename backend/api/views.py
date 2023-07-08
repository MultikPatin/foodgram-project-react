from django.shortcuts import render

from rest_framework import filters
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from django.contrib.auth import get_user_model

from recipes.models import (
    Ingredients,
    Tags,
)
from api.serializers import (
    IngredientsSerializer,
    TagsSerializer,
)




class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']

class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer




