from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


def get_token(username, password):
    session_user = authenticate(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=session_user)
    return token


def validate(data, fileds):
    for filed in fileds:
        if data.get(filed) is None or data.get(filed) == "":
            return True
    return False
