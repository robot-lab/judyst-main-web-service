from rest_framework import serializers
import json

from core.models import CustomUser, Links, Documents


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    read_only_fields = ('id',)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'username',
                  'organization', 'password', 'id')


def special_link_serializer(link):
    """
    function for serialise link models in special way

    :param link: Links
        link model for serialising

    :return: Dict
        dict for serializing
    """
    document = Documents.objects.all().get(doc_id=link.doc_id_from)
    document_to = Documents.objects.all().get(doc_id=link.doc_id_to)
    serializer = {
        'doc_id_from': link.doc_id_from,
        'doc_id_to': link.doc_id_to,
        'to_doc_title': document_to.title,
        'citations_number': link.citations_number,
        'positions_list': [json.loads(_) for _ in link.positions_list],
        'text': document.text
    }
    return serializer


def special_links_serializer(links):
    """
    function for serialise link models in special way

    :param links: Links
        links models for serialising

    :return: Dict
        list of dicts for serializing
    """
    return [special_link_serializer(link) for link in links ]
