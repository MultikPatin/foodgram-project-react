from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    SAFE_METHODS
)
from rest_framework.pagination import (
    LimitOffsetPagination
)
from rest_framework.response import Response
from rest_framework.request import Request

from .serializers import (
    PostUserSerializer,
    GetUserSerializer,
    PasswordSerializer,
    SubscriptionsSerializer,
    FollowerSerializer
)
from .models import Follow


User = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
    
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetUserSerializer
        return PostUserSerializer
    
    def perform_create(self, serializer):
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = GetUserSerializer(user)
        return Response(
            serializer.data
        )

    @action(
        ['post'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def set_password(self, request, *args, **kwargs):
        user = self.request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                'Пароль успешно изменен',
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        follow = Follow.objects.filter(user=request.user)
        user_obj = [x.following for x in follow]
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(user_obj, request)
        serializer = SubscriptionsSerializer(
            result_page,
            many=True,
            context=request.query_params
        )
        return paginator.get_paginated_response(serializer.data)


    @action(
        methods=['delete', 'post'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request: Request, pk=None):
        recipes_limit = request.query_params.get('recipes_limit')
        user = request.user
        following = get_object_or_404(User, pk=pk)
        follow = Follow.objects.filter(user=user, following=following)
        data = {
            'user': user.id,
            'following': following.id,
        }
        if request.method == 'POST':
            if follow.exists():
                return Response(
                    'Вы уже подписаны',
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FollowerSerializer(
                data=data,
                context=request.query_params
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            result_page = SubscriptionsSerializer(
                following,
                context={
                    'recipes_limit': recipes_limit,
                    'following': following
                }
            )
            return Response(
                result_page.data,
                status=status.HTTP_201_CREATED
            )  
        elif request.method == 'DELETE':
            follow.delete()
            return Response(
                'Успешная отписка',
                status=status.HTTP_204_NO_CONTENT
            )
