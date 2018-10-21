from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


def get_token(username, password):
    """
    function for generate token for user by email and password
    :param username: user email
    :param password: user password
    :return: token
    """
    session_user = authenticate(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=session_user)
    return token


def validate(data, fileds):
    """
    validator for checkin are these fields in data
    :param data: data for validate
    :param fileds: must have fields
    :return: False if data is correct
    """
    for filed in fileds:
        if data.get(filed) is None or data.get(filed) == "":
            return True
    return False
