from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, mixins, filters

from .serializers import (
    UserSerializer,
    SubscribeSerializer
)
from .models import Follow


User = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    pass





class SubscribeViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = SubscribeSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=get_object_or_404(
                User,
                id=self.kwargs.get("author_id")
            ),
            user=self.request.user
            )