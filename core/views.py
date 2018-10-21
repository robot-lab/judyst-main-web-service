from rest_framework import viewsets
from rest_framework.response import Response

from core.models import CustomUser as User
from core.serializers import UserSerializer
from core.utils.decorators import redirect_if_authorize
from core.utils.exceptions import ErrorResponse
from core.utils.functions import get_token, validate


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or register users.
    """

    def list(self, request):
        """
        simple method to see all users
        :param request: a plain web request
        :return: response with list of users
        """
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @redirect_if_authorize
    def registration(self, request):
        """
        method for user registration
        if user is authorize then we redirect him
        :param request: web request that contain user fileds:
                first_name
                last_name
                email
                password
                organization
        :return: token for authorized user
        """
        validate_data = request.data
        if validate(validate_data, ['first_name', 'last_name', 'email', 'password', 'organization']):
            return ErrorResponse().not_valid()
        # FIXME: (Lev) we need to add a check if this user exist already.
        try:
            user = User.objects.create(email=validate_data['email'], username=validate_data['email'],
                                       first_name=validate_data['first_name'], last_name=validate_data['last_name'],
                                       organization=validate_data['organization'])
            user.set_password(validate_data['organization'])
            user.save()
            token = get_token(validate_data['email'], validate_data['organization'])
        except Exception:
            return ErrorResponse().not_valid()
        # FIXME: (Lev) add a email sending function
        return Response({"token": token.key})

    @redirect_if_authorize
    def login(self, request):
        """
        method for user authorization
        if user is authorize then we redirect him
        :param request: web request that contain user fileds:
                email
                password
        :return: token for authorized user
        """
        validate_data = request.data
        if validate(validate_data, ['email', 'password']):
            return ErrorResponse().not_valid()
        try:
            token = get_token(validate_data['email'], validate_data['organization'])
        except Exception:
            return ErrorResponse().not_valid()
        return Response({"token": token.key})

    def logout(self, request):
        """
        method for user logout
        if user is authorize his token will be delete
        :param request: a plain web request
        :return: a response with status 200
        """
        request.user.auth_token.delete()
        # FIXME: (LEV) add check for user authorization
        return Response(status=200)
