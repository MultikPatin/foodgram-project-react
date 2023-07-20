from django.contrib.auth import get_user_model

from rest_framework import serializers

from users.models import Follow

from recipes.models import Recipes


User = get_user_model()

USER_FIELDS = [
    'email',
    'id',
    'username',
    'first_name',
    'last_name',
]

class CoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class IsSubscribedMixin():
    
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user,
            following=obj
        ).exists()


class RecipleInfoMixin():
    
    def get_recipes_count(self, obj):
        return obj.recipes.all().count()
    
    def get_recipes(self, obj):
        recipes_limit = int(
            self.context.get('recipes_limit')
        )
        resipes = Recipes.objects.values(
            'id',
            'name',
            'image',
            'cooking_time',
        )[:recipes_limit]
        return resipes