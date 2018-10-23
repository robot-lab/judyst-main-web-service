from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from rest_framework.authtoken.models import Token

from core.models import CustomUser as User


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
    validator for checking are these fields in data
    :param data: data for validate
    :param fileds: must have fields
    :return: False if data is correct
    """
    for filed in fileds:
        if data.get(filed) is None or data.get(filed) == "":
            return True
    return False


def send_email(message, user_email):
    """
    It's a function for sending email
    :param message: message for user
    :param user_email: email of user
    :return: None
    """
    email = EmailMessage('Verification', message,
                         from_email='judical.analyst@gmail.com',
                         to=[user_email])
    email.send()


def get_user_or_none(key):
    """
    util for get user or none if where no user
    :param key: user email as key
    :return: user or none
    """
    try:
        user = User.objects.all().get(username=key)
    except Exception:
        user = None
    return user
