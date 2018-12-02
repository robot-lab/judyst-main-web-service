from rest_framework import viewsets
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from django.http import FileResponse, HttpResponseNotFound
from judyst_web_service.settings import BASE_DIR
import os

import core.models
from core.models import CustomUser as User, Documents
from core.serializers import UserSerializer, special_links_serializer
from core.utils.decorators import redirect_if_authorize
from core.utils.exceptions import ErrorResponse, CommonAnalysisException
from core.utils.functions import get_token, is_not_valid_text_fields, \
    send_email, get_user_or_none, create_user_from_fields, check_email, \
    is_not_fields_include, check_password

from core.analysis import entry as analysis


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet
    """

    text_field_max_length = 255
    email_max_length = 150

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
                                         max_length=self.text_field_max_length,
                                         only_latin=True) or \
                is_not_valid_text_fields(validate_data, ['organization'],
                                         max_length=self.text_field_max_length
                                         ) or \
                not check_email(validate_data['email'],
                                max_length=self.email_max_length) or \
                not check_password(validate_data['password']):
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


class AnalysisViewSet(viewsets.ViewSet):
    def common_request(self, request):
        try:
            validate_data = request.data
            if is_not_fields_include(validate_data,
                                     ['method', 'parameters',
                                      'search_targets']):
                return ErrorResponse().not_valid()
            if is_not_fields_include(validate_data['search_targets'],
                                     ['sources', 'sources_pattern_type',
                                      'numbers', 'numbers_pattern_type',
                                      'dates', 'dates_pattern_type',
                                      ]):
                return ErrorResponse().not_valid()
            analysis_result = analysis.process(validate_data, core.models)
            return analysis_result
        except CommonAnalysisException as ex:
            # may be something else...
            return ErrorResponse().not_valid()




def main(request):
    return FileResponse(open(BASE_DIR+'/frontend/dist/static/index.html',
                             'rb'))


def static_delivery(request, path=""):
    if os.path.isfile(BASE_DIR+'frontend/dist/' + path):
        response = FileResponse(open(BASE_DIR+'/frontend/dist/' + path, 'rb'))
        if 'css'in path:
            response['Content-Type'] = 'text/css'
        if 'js' in path:
            response['Content-Type'] = 'text/javascript'

    else:
        response = HttpResponseNotFound
    return response

