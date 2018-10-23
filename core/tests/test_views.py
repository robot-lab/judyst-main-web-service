from django.core import mail
from django.test import TestCase
from django.urls import reverse
from core.models import CustomUser
import json
from core.tests.utils import get_dict_from_user, user_fields, login_fields
from rest_framework.authtoken.models import Token
# TODO (Danila) Add fields checks tests for registration and authorisation.
# TODO (Danila) Find way how user authorisation could be tested.


class TestNoUser(TestCase):

    def test_list(self):
        resp = self.client.get(reverse('core:list'))

        assert b'[]' == resp.content
        self.assertEqual(200, resp.status_code)

    def test_login_no_user(self):
        context = login_fields.copy()

        resp = self.client.post(reverse('core:login'), context)

        assert 400 == resp.status_code
        assert '{"code":400,"message":"invalid request"}' == \
               resp.content.decode()


class TestExistUsers(TestCase):

    @classmethod
    def setUpClass(cls):
        user = CustomUser.objects.create(email=login_fields['email'],
                                         username=login_fields['email'],
                                         first_name='name',
                                         last_name='surname',
                                         organization='My organisation')
        user.set_password(login_fields['password'])
        user.save()

    @classmethod
    def tearDownClass(cls):
        users = CustomUser.objects.all()
        for user in users:
            user.delete()

    def tearDown(self):
        mail.outbox.clear()

        users = CustomUser.objects.all()
        for user in users:
            if user.username != login_fields['email']:
                user.delete()

    def test_url_list_exist_at_desired_location(self):
        resp = self.client.get('/api/user/list')
        self.assertEqual(200, resp.status_code)

    def test_url_list_access_by_name(self):
        resp = self.client.get(reverse('core:list'))
        self.assertEqual(200, resp.status_code)

    def test_url_logout_exist_at_desired_location(self):
        resp = self.client.get('/api/user/logout')
        self.assertEqual(200, resp.status_code)

    def test_url_logout_access_by_name(self):
        resp = self.client.get(reverse('core:logout'))
        self.assertEqual(200, resp.status_code)

    def test_url_register_exist_at_desired_location(self):
        context = user_fields.copy()
        resp = self.client.post('/api/user/register', context)
        self.assertEqual(200, resp.status_code)

    def test_url_register_access_by_name(self):
        context = user_fields.copy()
        resp = self.client.post(reverse('core:register'), context)
        self.assertEqual(200, resp.status_code)

    def test_url_login_exist_at_desired_location(self):
        context = login_fields.copy()
        resp = self.client.post('/api/user/login', context)
        self.assertEqual(200, resp.status_code)

    def test_url_login_access_by_name(self):
        context = login_fields.copy()
        resp = self.client.post(reverse('core:login'), context)
        self.assertEqual(200, resp.status_code)

    def test_list(self):
        users = CustomUser.objects.all()
        expected = []
        for user in users:
            expected.append(get_dict_from_user(user))

        resp = self.client.get(reverse('core:list'))
        actual = json.loads(resp.content.decode())

        assert expected == actual
        self.assertEqual(200, resp.status_code)

    def test_correct_registration(self):
        context = user_fields.copy()

        resp = self.client.post(reverse('core:register'), context)

        users = CustomUser.objects.filter(username=context['email'])

        assert 1 == len(users)

        user = users[0]

        user_dict = get_dict_from_user(user)
        for field in user_fields:
            if field != 'password':
                assert user_fields[field] == user_dict[field]
            else:
                assert user.check_password(user_fields[field])

        expected_token, _ = Token.objects.get_or_create(user=user)

        assert 200 == resp.status_code

        assert '{"token":"' + str(expected_token) + '"}' == \
               resp.content.decode()

        self.assertEqual(len(mail.outbox), 1)

        message = mail.outbox[0]

        self.assertEqual(message.body, "Not Implemented:  500")
        self.assertEqual(message.to[0], user_fields['email'])

    def test_registration_with_used_email(self):
        context = user_fields.copy()
        context['email'] = 'badEmail@gmail.com'

        resp = self.client.post(reverse('core:register'), context)

        assert 0 == len(mail.outbox)

        assert 400 == resp.status_code
        assert '{"code":400,"message":"user already exist"}' == \
               resp.content.decode()

    def test_login_correct(self):
        context = login_fields.copy()

        resp = self.client.post(reverse('core:login'), context)

        users = CustomUser.objects.filter(username=context['email'])

        assert 1 == len(users)

        user = users[0]
        expected_token, _ = Token.objects.get_or_create(user=user)

        assert 200 == resp.status_code
        assert '{"token":"' + str(expected_token) + '"}' == \
               resp.content.decode()
