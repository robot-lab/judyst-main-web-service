from rest_framework import serializers

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
    serializer = {
        'doc_id_from': link.doc_id_from,
        'doc_id_to': link.doc_id_to,
        'to_doc_title': link.to_doc_title,
        'citations_number': link.citations_number,
        'positions_list': link.positions_list,
        'text': document.tex
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