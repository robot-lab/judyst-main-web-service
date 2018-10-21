from rest_framework import viewsets
from rest_framework.response import Response

from core.exceptions import ErrorResponse
from core.models import CustomUser as User
from core.serializers import UserSerializer
from core.utils.decorators import redirect_if_authorize
from core.utils.functions import get_token, validate


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or register users.
    """

    def list(self, request):
        """
        simple method to see all users
        :param request:
        :return: response with list of users
        """
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @redirect_if_authorize
    def registration(self, request):
        """
        method for registration
        :param request: information about users
        :return:
        """
        validate_data = request.data
        if validate(validate_data, ['first_name', 'last_name', 'email', 'password', 'organization']):
            return ErrorResponse().not_valid()
        # TODO(Lev) we need to add a check if this user exist already.
        try:
            user = User.objects.create(email=validate_data['email'], username=validate_data['email'],
                                       first_name=validate_data['first_name'], last_name=validate_data['last_name'],
                                       organization=validate_data['organization'])
            user.set_password(validate_data['organization'])
            user.save()
            token = get_token(validate_data['email'], validate_data['organization'])
        except Exception:
            return ErrorResponse().not_valid()
        # TODO(Lev) add a email sending function
        return Response({"token": token.key})

    @redirect_if_authorize
    def login(self, request):
        validate_data = request.data
        if validate(validate_data, ['email', 'password']):
            return ErrorResponse().not_valid()
        try:
            token = get_token(validate_data['email'], validate_data['organization'])
        except Exception:
            return ErrorResponse().not_valid()
        return Response({"token": token.key})

    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=200)
