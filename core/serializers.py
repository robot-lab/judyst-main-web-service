from rest_framework import serializers
from core.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    read_only_fields = ('id',)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'username', 'organization','password','id')
