from rest_framework import serializers

from core.models import CustomUser, Links


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    read_only_fields = ('id',)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'username', 'organization', 'password', 'id')


class LinksSerializer(serializers.ModelSerializer):
    read_only_fields = ('id',)

    class Meta:
        model = Links
        fields = ('doc_id_from', 'doc_id_to', 'to_doc_title', 'citations_number', 'contexts_list', 'positions_list')
