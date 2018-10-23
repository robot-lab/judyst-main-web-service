from rest_framework import viewsets
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response

from core.models import CustomUser as User, Links
from core.serializers import UserSerializer, LinksSerializer
from core.utils.decorators import redirect_if_authorize
from core.utils.exceptions import ErrorResponse
from core.utils.functions import get_token, is_not_valid_text_fields, \
    send_email, get_user_or_none, create_user_from_fields, check_email


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet
    """
    def list(self, request):
        """
        Simple method to see all users.

        :param request: HttpRequest
            A plain web request.

        :return: HttpResponse
            Response with list of users.
        """
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @redirect_if_authorize
    def registration(self, request):
        """
        Method for user registration. If user is authorize then we redirect
        him.

        :param request: HttpRequest
            Web request that contain user fields: first_name, last_name, email,
            password, organization.

        :return: HttpResponse
            Token for authorized user.
        """
        validate_data = request.data
        if is_not_valid_text_fields(validate_data, ['email', 'password']) or \
                is_not_valid_text_fields(validate_data,
                                         ['first_name', 'last_name'],
                                         max_length=255, only_latin=True) or \
                is_not_valid_text_fields(validate_data, ['organization'],
                                         max_length=255) or \
                not check_email(validate_data['email']):
            return ErrorResponse().not_valid()
        if get_user_or_none(validate_data['email']) is not None:
            return ErrorResponse().user_exist()
        try:
            create_user_from_fields(validate_data)
            token = get_token(validate_data['email'],
                              validate_data['password'])
        except Exception:
            return ErrorResponse().not_valid()
        send_email("Not Implemented:  500", validate_data['email'])
        return Response({"token": token.key})

    @redirect_if_authorize
    def login(self, request):
        """
        Method for user authorization. If user is authorize then we redirect
        him.

        :param request: HttpRequest
            Web request that contain user fields: email, password.

        :return: HttpResponse
            Token for authorized user.
        """
        validate_data = request.data
        if is_not_valid_text_fields(validate_data, ['email', 'password']):
            return ErrorResponse().not_valid()
        try:
            token = get_token(validate_data['email'],
                              validate_data['password'])
        except Exception:
            return ErrorResponse().not_valid()
        return Response({"token": token.key})

    def logout(self, request):
        """
        Method for user logout. If user is authorize his token will be delete.

        :param request: HtpRequest
            A plain web request.

        :return: HttpResponse
            A response with status 200.
        """
        if 'Token' in get_authorization_header(request).decode():
            request.user.auth_token.delete()
        return Response(status=200)


class SearchViewSet(viewsets.ViewSet):

    def search(self, request):
        # TO DO: make this function better
        validate_data = request.data
        print(validate_data)
        if is_not_valid_text_fields(validate_data, ['doc_id_from', 'doc_id_to']):
            return ErrorResponse().not_valid()
        # TO DO: add check for empty(!)
        if validate_data['doc_id_from'] != -1 and validate_data['doc_id_to'] != -1:
            queryset = Links.objects.all().filter(doc_id_from=validate_data['doc_id_from'],
                                                  doc_id_to=validate_data['doc_id_to'])
        elif validate_data['doc_id_from'] != -1:
            queryset = Links.objects.all().filter(doc_id_from=validate_data['doc_id_from'])
        elif validate_data['doc_id_to'] != -1:
            queryset = Links.objects.all().filter(doc_id_to=validate_data['doc_id_to'])
        else:
            queryset = None
        serializer = LinksSerializer(queryset, many=queryset.count() > 1)
        return Response(serializer.data)

    def put(self, request):
        # костыль TO DO: DELETE
        f = open('/home/korwin/jsonAllCleanLinks.json', 'r')
        import json
        js = json.loads(f.read())
        print(len(js))
        for _, item in enumerate(js):
            Links.objects.create(doc_id_from=item['doc_id_from'], doc_id_to=item['doc_id_to'],
                                 to_doc_title=item['to_doc_title'], citations_number=item['citations_number'],
                                 contexts_list=item['contexts_list'], positions_list=item['positions_list'])
            print(_)
        queryset = Links.objects.all()
        serializer = LinksSerializer(queryset)
        return Response(serializer.data)
