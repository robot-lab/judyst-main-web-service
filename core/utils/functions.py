import re

from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from rest_framework.authtoken.models import Token

from core.models import CustomUser as User, Links


class CheckText:
    """
    Class for checking is string consist of latin characters.
    """

    validators = {'IsLatin': re.compile(r'^[a-zA-Z]*$'),
                  'Password':
                      re.compile(r'^[\#-\&\[\]\_\:\;a-zA-Z,0-9]{8,64}$')}

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
        if not isinstance(line, str) or line == "":
            return True
        if max_length is not None and len(line) > max_length:
            return True
        if min_length is not None and len(line) < min_length:
            return True
        if only_latin and not CheckText.check_line(line):
            return True
    return False


def is_not_fields_include(data, fields):
    """
    Function for checking including list of fields in data dictionary.

    :param data: Dict
        Dictionary for checking.

    :param fields: list
        List of fields for checking.

    :return: boolean
        True if exist field in fields which is not present in  data, False
        otherwise.
    """
    for filed in fields:
        line = data.get(filed)
        if line is None:
            return True
        if isinstance(line, str) and line == "":
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


def check_email(line, max_length=None):
    """
    Function for validation users email.

    :param line: str
        String for checking if it is email.

    :param max_length: int
        Max length of email.

    :return: Boolean
        True if it is correct email, False otherwise.
    """
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(line)
        if max_length:
            return len(line) <= max_length
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


def create_link_from_fields(fields):
    """
    Function for creating link from given fields. Fields are not checked.

    :param fields: Dict
        Dictionary with fields for link.

    :return: Link
        Created link.
    """
    return Links.objects.create(doc_id_from=fields['doc_id_from'],
                                doc_id_to=fields['doc_id_to'],
                                to_doc_title=fields['to_doc_title'],
                                citations_number=fields['citations_number'],
                                positions_list=fields['positions_list'])


def get_links(validate_data):
    """
    function for getting links from db

    :param validate_data: Dict
         validate data from request

    :return: queryset
        queryset of Links model
    """
    if validate_data['doc_id_from'] != -1 and\
            validate_data['doc_id_to'] != -1:
        queryset = Links.objects.all().filter(
            doc_id_from=validate_data['doc_id_from'])\
            .filter(doc_id_to=validate_data['doc_id_to'])
    elif validate_data['doc_id_from'] != -1:
        queryset = Links.objects.all().filter(
            doc_id_from=validate_data['doc_id_from'])
    elif validate_data['doc_id_to'] != -1:
        queryset = Links.objects.all().filter(
            doc_id_to=validate_data['doc_id_to'])
    else:
        queryset = []
    return queryset
