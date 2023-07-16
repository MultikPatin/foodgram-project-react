from django.contrib.auth import get_user_model

from rest_framework import serializers


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
