from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, mixins, filters
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    SAFE_METHODS
)

from .serializers import (
    CustomUserSerializer,
    GetUserSerializer,
    SubscribeSerializer
)

from .models import Follow


User = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetUserSerializer
        return CustomUserSerializer
    
    def perform_create(self, serializer):
        if "password" in self.request.data:
            password = make_password(self.request.data["password"])
            serializer.save(password=password)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if "password" in self.request.data:
            password = make_password(self.request.data["password"])
            serializer.save(password=password)
        else:
            serializer.save()





# class SubscribeViewSet(mixins.CreateModelMixin,
#                        mixins.DestroyModelMixin,
#                        viewsets.GenericViewSet):
#     queryset = Follow.objects.all()
#     serializer_class = SubscribeSerializer

#     def perform_create(self, serializer):
#         serializer.save(
#             author=get_object_or_404(
#                 User,
#                 id=self.kwargs.get("author_id")
#             ),
#             user=self.request.user
#             )