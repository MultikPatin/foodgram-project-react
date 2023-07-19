from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework import status, viewsets, mixins, filters
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    SAFE_METHODS
)
from rest_framework.pagination import (
    # PageNumberPagination,
    LimitOffsetPagination
)
from rest_framework.response import Response

from .serializers import (
    PostUserSerializer,
    GetUserSerializer,
    PasswordSerializer,
    SubscriptionsSerializer
)

from .models import Follow


User = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [
        AllowAny]
    pagination_class = LimitOffsetPagination
    
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetUserSerializer
        return PostUserSerializer
    
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

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = GetUserSerializer(user)
        return Response(serializer.data)

    @action(
        ["post"],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def set_password(self, request, *args, **kwargs):
        user = self.request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response()
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        follow = Follow.objects.filter(user=user)
        user_obj = []
        for follow_obj in follow:
            user_obj.append(follow_obj.following)
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(user_obj, request)
        serializer = SubscriptionsSerializer(
            result_page,
            many=True,
            # context={"current_user": user}
        )
        return paginator.get_paginated_response(serializer.data)