from core .exceptions import ErrorResponse
from rest_framework import viewsets
from core.models import CustomUser as User
from core.serializers import UserSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token


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


    def registration(self, request):
        """
        method for registration
        :param request: information about users
        :return:
        """
        try:
            validate_data = request.data
            first_name = validate_data['first_name']
            last_name = validate_data['last_name']
            email = validate_data['email']
            username = validate_data['email'].split('@')[0]
            password = validate_data['password']
            organization = validate_data['organization']
        except Exception as e:
            print(e)
            return ErrorResponse().not_valid()
        try:
            user = User.objects.create(email=email,username=username,
                                       first_name=first_name,last_name=last_name,  organization=organization)
            user.set_password(password)
            user.save()
            session_user = authenticate(username=username, password=password)
            token, _ = Token.objects.get_or_create(user=session_user)
        except Exception as e:
            print(e)
            return ErrorResponse().not_valid()

        return Response({"token": token.key})

    def login(self,request):
        try:
            validate_data = request.data
            email = validate_data['email']
            username = validate_data['email'].split('@')[0]
            password = validate_data['password']
        except Exception:
            return ErrorResponse.not_valid()
        try:
            session_user = authenticate(username=username, password=password)
            token, _ = Token.objects.get_or_create(user=session_user)
        except Exception as e:
            print(e)
            return ErrorResponse().not_valid()
        return Response({"token": token.key})

    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=200)


