import re

from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from rest_framework.authtoken.models import Token

from core.models import CustomUser as User


class IsLatin:

    check = re.compile(r'^[a-zA-Z]*$')

    @classmethod
    def check_line(cls, line):
        return bool(cls.check.match(line))


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


def is_not_valid_text_fields(data, fields, max_length=None, min_length=None,
                             only_latin=False):
    """
    validator for checking are these fields in data
    :param data: data for validate
    :param fields: must have fields
    :param max_length: max_length of string field
    :param min_length: min_length of string field
    :param only_latin: Flag if this field may contain only latin characters.
    :return: False if data is correct
    """
    for filed in fields:
        line = data.get(filed)
        if not isinstance(line, str) or line == "":
            return True
        if max_length is not None and len(line) > max_length:
            return True
        if min_length is not None and len(line) < min_length:
            return True
        if only_latin and not IsLatin.check_line(line):
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


def check_email(line):
    """
    Function for validation users email.
    :param line: str
        String for checking if it is email.
    :return: Boolean
        True if it is correct email, False otherwise.
    """
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(line)
        return True
    except ValidationError:
        return False


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


def create_user_from_fields(fields):
    """
    Function for creating user from given fields. Fields are not checked.

    :param fields: dict
        Dictionary with fields for user.

    :return CustomUser
        Created user.
    """
    user = User.objects.create(email=fields['email'], username=fields['email'],
                               first_name=fields['first_name'],
                               last_name=fields['last_name'],
                               organization=fields['organization'])
    user.set_password(fields['password'])
    user.save()
    return user
