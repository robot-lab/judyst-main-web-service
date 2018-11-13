"""
Test functions connected to link model.
"""
import pytest

from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token

from core.tests.utils import get_dict_from_user, another_user_fields, \
    default_user_fields, default_user_in_bd, TestConstants
from core.models import CustomUser
from core.utils.functions import get_token, send_email, get_user_or_none, \
    create_user_from_fields, check_email, CheckText


@pytest.mark.critical_test
@pytest.mark.django_db
def test_get_token(default_user_in_bd):
    session_user = authenticate(username=default_user_fields['email'],
                                password=default_user_fields['password'])
    expected_token, _ = Token.objects.get_or_create(user=session_user)

    actual_token = get_token(default_user_fields['email'],
                             default_user_fields['password'])

    assert expected_token == actual_token


class TestGetUserOrNone:
    @pytest.mark.django_db
    def test_get_user(self, default_user_in_bd):
        actual_user = get_user_or_none(default_user_fields['email'])
        expected_user = CustomUser.objects.get(
            email=default_user_fields['email'])
        assert expected_user == actual_user

    @pytest.mark.django_db
    def test_no_user(self, default_user_in_bd):
        actual_user = get_user_or_none(another_user_fields['email'])
        assert actual_user is None



def test_send_email(mailoutbox):
    send_email(TestConstants.email_message, TestConstants.email_address)

    # Check that was added exactly one message.
    assert 1 == len(mailoutbox)

    message = mailoutbox[0]

    # Check that was send to exactly one address.
    assert 1 == len(message.to)
    assert TestConstants.email_address == message.to[0]
    assert TestConstants.email_message == message.body


@pytest.mark.critical_test
@pytest.mark.django_db
def test_create_user_from_fields(default_user_in_bd):
    actual_user = create_user_from_fields(another_user_fields)
    users = CustomUser.objects.filter(email=another_user_fields['email'])

    # Check tha was added exactly one user.
    assert 1 == len(users)

    user = users[0]

    user_dict = get_dict_from_user(user)
    for field in another_user_fields:
        if field != 'password':
            assert another_user_fields[field] == user_dict[field]
        else:
            assert user.check_password(another_user_fields[field])

    assert get_dict_from_user(actual_user) == user_dict


@pytest.fixture(scope="function",
                params=[('test@gmail.com', 150, True),
                        ('test123', 150, False),
                        ('q'*140+'@gamil.com', 150, True),
                        ('q'*141+'@gmail.com', 150, False),
                        ('q@t.ui', 150, True)],
                ids=["correct", "incorrect", 'long email',
                     'long incorrect email', 'short email'])
def param_check_email(request):
    return request.param


def test_check_email(param_check_email):
    line, max_length, result = param_check_email
    assert result == check_email(line, max_length=max_length)


@pytest.fixture(scope="function",
                params=[('qwerty1', False),
                        ('qwerty', True),
                        ('клмн', False)],
                ids=["with digit", "latin", "russian text"])
def param_is_latin(request):
    return request.param


def test_is_latin(param_is_latin):
    data, result = param_is_latin
    assert result == CheckText.check_line(data)


@pytest.mark.django_db
def test_get_dict_from_user(default_user_in_bd):
    user = CustomUser.objects.get(email=default_user_fields['email'])
    actual_result = get_dict_from_user(user)

    expected_result = {'first_name': user.first_name,
                       'last_name': user.last_name,
                       'email': user.email, 'username': user.username,
                       'id': user.id, 'organization': user.organization}

    assert expected_result == actual_result
