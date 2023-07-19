from django.contrib.auth import get_user_model

from rest_framework import serializers

from users.models import Follow


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
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user,
            following=obj
        ).exists()