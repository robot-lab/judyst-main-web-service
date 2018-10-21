from django.shortcuts import render
from core .exceptions import ErrorResponse
# Create your views here.

from rest_framework import viewsets
from core.models import CustomUser as User
from core.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import login, authenticate

class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def registration(self, request):
        try:
            validate_data = request.data
            print(request.data)
            first_name = validate_data['first_name']
            last_name = validate_data['last_name']
            email = validate_data['email']
            username = validate_data['username']
            password = validate_data['password']
            organization = validate_data['organization']
            print(first_name,last_name, email,password,username,organization)
        except Exception as e:
            print(e)
            return ErrorResponse().not_valid()
        try:
            user = User.objects.create(email=email,username=username,
                        first_name=first_name,last_name=last_name,  organization=organization)
            user.set_password(password)
            user.save()
            session_user = authenticate(username=username, password=password)
            login(request, session_user)
        except Exception as e:
            print(e)
            return ErrorResponse().not_valid()

        return Response(UserSerializer(session_user).data)
