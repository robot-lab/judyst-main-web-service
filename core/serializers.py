from rest_framework import serializers
from core import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('email', 'first_name', 'last_name', 'username', 'email', 'organization' )