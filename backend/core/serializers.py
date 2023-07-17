from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()

class CoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
