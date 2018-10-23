from django.core import mail
from django.contrib.auth import authenticate
from django.test import TestCase
from core.models import CustomUser
from rest_framework.authtoken.models import Token
from core.utils.functions import get_token, validate, send_email, \
    get_user_or_none
from core.tests.utils import get_dict_from_user


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
        right_token, _ = Token.objects.get_or_create(user=session_user)

        token = get_token('goodEmail@gmail.com', 'p4thw0rd')

        self.assertEqual(right_token, token)


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
        right_user = CustomUser.objects.get(email='goodEmail@gmail.com')
        self.assertEqual(right_user, actual_user)

    def test_no_user(self):
        actual_user = get_user_or_none('badEmail@gmail.com')
        right_user = None
        self.assertEqual(right_user, actual_user)


class TestSendEmail(TestCase):

    @classmethod
    def setUpClass(cls):
        mail.outbox.clear()

    @classmethod
    def tearDownClass(cls):
        mail.outbox.clear()

    def test_send_email(self):
        send_email('qwerty12345', 'goodEmail@gmail.com')

        self.assertEqual(len(mail.outbox), 1)

        message = mail.outbox[0]

        self.assertEqual(message.body, 'qwerty12345')
        self.assertEqual(message.to[0], 'goodEmail@gmail.com')


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
        result = {'first_name': user.first_name, 'last_name': user.last_name,
                  'email': user.email, 'username': user.username,
                  'id': user.id, 'organization': user.organization}

        self.assertEqual(result, get_dict_from_user(user))
