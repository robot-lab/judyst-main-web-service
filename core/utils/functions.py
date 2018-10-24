import re

from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from rest_framework.authtoken.models import Token

from core.models import CustomUser as User


class CheckText:
    """
    Class for checking is string consist of latin characters.
    """

    validators = {'IsLatin': re.compile(r'^[a-zA-Z]*$'),
                  'Password': re.compile(r'^[\#-\&\[\]\_\:\;a-zA-Z,0-9]{8,64}$')}

    @classmethod
    def check_line(cls, line, check='IsLatin'):
        """
        Function for checking if string consist of latin characters.

        :param line: str
            String for checking.

        :param check: str
            Type of checking.

        :return: bool
            True if string consist only of latin characters, false otherwise.
        """
        return bool(cls.validators[check].match(line))


def get_token(username, password):
    """
    Function for generate token for user by email and password.

    :param username: str
        User email.

    :param password: str
        User password.

    :return: Token
        User's token.
    """
    session_user = authenticate(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=session_user)
    return token


def is_not_valid_text_fields(data, fields, max_length=None, min_length=None,
                             only_latin=False):
    """
    Validator for checking are these fields in data.

    :param data: dict
        Data for validate.

    :param fields: list
        Must have fields.

    :param max_length: int ot None
        Max_length of string field, if specified.

    :param min_length: int or None
        Min_length of string field, is specified.

    :param only_latin: bool
        Flag if this field may contain only latin characters.

    :return:
        False if data is correct
    """
    for filed in fields:
        line = data.get(filed)
        if line is None or line == "":
            return True
        if max_length is not None and len(line) > max_length:
            return True
        if min_length is not None and len(line) < min_length:
            return True
        if only_latin and not CheckText.check_line(line):
            return True
    return False


def send_email(message, user_email):
    """
    It's a function for sending email.

    :param message: str
        Message for user.

    :param user_email: str
        Email of user.
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


def check_password(line):
    """
    Function for validation users password.

    :param line: str
        String for checking if it is password.

    :return: Boolean
        True if it is correct password, False otherwise.
    """
    return CheckText.check_line(line, 'Password')


def get_user_or_none(key):
    """
    Function for get user or none if where no user.

    :param key: str
        Username for searching.

    :return: CustomUser or none
        User if it was found, None otherwise.
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

    :return: CustomUser
        Created user.
    """
    user = User.objects.create(email=fields['email'], username=fields['email'],
                               first_name=fields['first_name'],
                               last_name=fields['last_name'],
                               organization=fields['organization'])
    user.set_password(fields['password'])
    user.save()
    return user
