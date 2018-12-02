from rest_framework import viewsets
from rest_framework.response import Response
from django.http import FileResponse, HttpResponseNotFound
from judyst_web_service.settings import BASE_DIR
import os

from core.models import Documents, Links
from core.serializers import special_links_serializer
from core.utils.exceptions import ErrorResponse
from core.utils.functions import is_not_valid_text_fields,\
     is_not_fields_include
from core.search.functions import get_links, get_document_by_id,\
     get_document_by_interredaction_id


class SearchViewSet(viewsets.ViewSet):

    def search(self, request):
        validate_data = request.data
        if is_not_fields_include(validate_data,
                                 ['doc_id_from', 'doc_id_to', 'range']):
            return ErrorResponse().not_valid()
        queryset = get_links(validate_data)
        try:
            serializer = special_links_serializer(
                queryset[validate_data['range'][0]: validate_data['range'][1]])
        except TypeError:
            return ErrorResponse().not_valid()
        return Response(serializer)

    def number_of_links(self, request):
        # request for all links(if both fields =-1) may cause "out of memory"
        validate_data = request.data
        if is_not_fields_include(validate_data, ['doc_id_from', 'doc_id_to']):
            return ErrorResponse().not_valid()
        queryset = get_links(validate_data)
        return Response({"size": len(queryset)})

    def document(self, request):
        try:
            validate_data = request.data
            if is_not_fields_include(validate_data, ['doc_id']):
                return ErrorResponse().not_valid()
            document = get_document_by_interredaction_id(validate_data)
            if document:
                return Response(document)
            document = get_document_by_id(validate_data)
            if not document:
                return ErrorResponse().not_found(data_caption='Document')
            return Response(document)
        except Documents.DoesNotExist:
            return ErrorResponse().not_found(data_caption='Document')

    