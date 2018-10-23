from django.core import mail
from django.contrib.auth import authenticate
from django.test import TestCase

from rest_framework.authtoken.models import Token

from core.tests.utils import get_dict_from_user, user_fields, login_fields
from core.models import CustomUser
from core.utils.functions import get_token, validate, send_email, \
    get_user_or_none
# TODO (Danila) Add tests for validation function.


class TestGetToken(TestCase):
    @classmethod
    def setUpClass(cls):
        user = CustomUser.objects.create(email='goodEmail@gmail.com',
                                         username='goodEmail@gmail.com',
                                         first_name='name',
                                         last_name='surname',
                                         organization='My organisation')
        user.set_password('p4thw0rd')
        user.save()

    @classmethod
    def tearDownClass(cls):
        users = CustomUser.objects.all()
        for user in users:
            user.delete()

    def test_get_token(self):
        session_user = authenticate(username='goodEmail@gmail.com',
                                    password='p4thw0rd')
        expected_token, _ = Token.objects.get_or_create(user=session_user)

        actual_token = get_token('goodEmail@gmail.com', 'p4thw0rd')

        assert expected_token == actual_token


class TestGetUserOrNone(TestCase):
    @classmethod
    def setUpClass(cls):
        user = CustomUser.objects.create(email='goodEmail@gmail.com',
                                         username='goodEmail@gmail.com',
                                         first_name='name',
                                         last_name='surname',
                                         organization='My organisation')
        user.set_password('p4thw0rd')
        user.save()

    @classmethod
    def tearDownClass(cls):
        users = CustomUser.objects.all()
        for user in users:
            user.delete()

    def test_get_user(self):
        actual_user = get_user_or_none('goodEmail@gmail.com')
        expected_user = CustomUser.objects.get(email='goodEmail@gmail.com')
        assert expected_user == actual_user

    def test_no_user(self):
        actual_user = get_user_or_none('badEmail@gmail.com')
        assert actual_user is None


class TestSendEmail(TestCase):

    @classmethod
    def setUpClass(cls):
        mail.outbox.clear()

    @classmethod
    def tearDownClass(cls):
        mail.outbox.clear()

    def test_send_email(self):
        send_email('qwerty12345', 'goodEmail@gmail.com')

        assert 1 == len(mail.outbox)

        message = mail.outbox[0]

        assert 'qwerty12345' == message.body
        assert 1 == len(message.to)
        assert 'goodEmail@gmail.com' == message.to[0]


class TestGetDictFromUser(TestCase):
    @classmethod
    def setUpClass(cls):
        user = CustomUser.objects.create(email='goodEmail@gmail.com',
                                         username='goodEmail@gmail.com',
                                         first_name='name',
                                         last_name='surname',
                                         organization='My organisation')
        user.set_password('p4thw0rd')
        user.save()

    @classmethod
    def tearDownClass(cls):
        users = CustomUser.objects.all()
        for user in users:
            user.delete()

    def test_get_dict_from_user(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        actual_result = get_dict_from_user(user)

        expected_result = {'first_name': user.first_name,
                           'last_name': user.last_name,
                           'email': user.email, 'username': user.username,
                           'id': user.id, 'organization': user.organization}

        assert expected_result == actual_result


def test_user_fields():
    assert 'email' in user_fields
    assert 'password' in user_fields
    assert 'first_name' in user_fields
    assert 'last_name' in user_fields
    assert 'organization' in user_fields


def test_login_fields():
    assert 'email' in login_fields
    assert 'password' in login_fields
