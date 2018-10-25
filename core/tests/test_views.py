from json import loads as parser_to_dict
from json import dumps as convert_to_json

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from rest_framework.authtoken.models import Token

from core.models import CustomUser, Links
from core.utils.functions import create_user_from_fields
from core.tests.utils import get_dict_from_user, user_fields, login_fields, \
    default_user_fields, set_links_in_db_from_file, search_link_fields

# TODO (Danila) Create tests for search


def check_registration(resp, context):
    """
    Function for checking registration process.

    :param resp: Response
        Response of test client for analysing.

    :param context: dict
        Dict with fields for new user.
    """
    users = CustomUser.objects.filter(username=context['email'])

    assert 1 == len(users)

    user = users[0]

    user_dict = get_dict_from_user(user)
    for field in user_fields:
        if field != 'password':
            assert context[field] == user_dict[field]
        else:
            assert user.check_password(context[field])

    expected_token, _ = Token.objects.get_or_create(user=user)

    assert 200 == resp.status_code

    assert '{"token":"' + str(expected_token) + '"}' == \
           resp.content.decode()

    assert 1 == len(mail.outbox)

    message = mail.outbox[0]

    assert 'Not Implemented:  500' == message.body
    assert 1 == len(message.to)
    assert user_fields['email'] == message.to[0]


class TestNoUser(TestCase):

    def test_list(self):
        resp = self.client.get(reverse('core_user:list'))

        assert b'[]' == resp.content
        assert 200 == resp.status_code

    def test_login_no_user(self):
        context = login_fields.copy()

        resp = self.client.post(reverse('core_user:login'),
                                convert_to_json(context),
                                content_type="application/json")

        assert 400 == resp.status_code
        assert '{"code":400,"message":"invalid request"}' == \
               resp.content.decode()


class TestExistUsers(TestCase):

    @classmethod
    def setUpClass(cls):
        create_user_from_fields(default_user_fields)

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
        assert 200 == resp.status_code

    def test_url_list_access_by_name(self):
        resp = self.client.get(reverse('core_user:list'))
        assert 200 == resp.status_code

    def test_url_logout_exist_at_desired_location(self):
        resp = self.client.get('/api/user/logout')
        assert 200 == resp.status_code

    def test_url_logout_access_by_name(self):
        resp = self.client.get(reverse('core_user:logout'))
        assert 200 == resp.status_code

    def test_url_register_exist_at_desired_location(self):
        context = user_fields.copy()
        resp = self.client.post('/api/user/register',
                                convert_to_json(context),
                                content_type="application/json")
        assert 200 == resp.status_code

    def test_url_register_access_by_name(self):
        context = user_fields.copy()
        resp = self.client.post(reverse('core_user:register'),
                                convert_to_json(context),
                                content_type="application/json")
        assert 200 == resp.status_code

    def test_url_login_exist_at_desired_location(self):
        context = login_fields.copy()
        resp = self.client.post('/api/user/login', convert_to_json(context),
                                content_type="application/json")
        assert 200 == resp.status_code

    def test_url_login_access_by_name(self):
        context = login_fields.copy()
        resp = self.client.post(reverse('core_user:login'),
                                convert_to_json(context),
                                content_type="application/json")
        assert 200 == resp.status_code

    def test_list(self):
        users = CustomUser.objects.all()
        expected = []
        for user in users:
            expected.append(get_dict_from_user(user))

        resp = self.client.get(reverse('core_user:list'))
        actual = parser_to_dict(resp.content.decode())

        assert expected == actual
        assert 200 == resp.status_code

    def test_correct_registration(self):
        context = user_fields.copy()

        resp = self.client.post(reverse('core_user:register'),
                                convert_to_json(context),
                                content_type="application/json")

        check_registration(resp, context)

    def test_registration_with_used_email(self):
        context = user_fields.copy()
        context['email'] = default_user_fields['email']

        resp = self.client.post(reverse('core_user:register'),
                                convert_to_json(context),
                                content_type="application/json")

        assert not mail.outbox

        assert 400 == resp.status_code
        assert '{"code":400,"message":"user already exist"}' == \
               resp.content.decode()

    def test_login_correct(self):
        context = login_fields.copy()

        resp = self.client.post(reverse('core_user:login'),
                                convert_to_json(context),
                                content_type="application/json")

        users = CustomUser.objects.filter(username=context['email'])

        assert 1 == len(users)

        user = users[0]
        expected_token, _ = Token.objects.get_or_create(user=user)

        assert 200 == resp.status_code
        assert '{"token":"' + str(expected_token) + '"}' == \
               resp.content.decode()

    def test_login_no_fields(self):
        resp = self.client.post(reverse('core_user:login'), {})

        assert 400 == resp.status_code
        assert '{"code":400,"message":"invalid request"}' == \
               resp.content.decode()

    def test_login_empty_fields(self):
        resp = self.client.post(reverse('core_user:login'),
                                {'email': '', 'password': ''})

        assert 400 == resp.status_code
        assert '{"code":400,"message":"invalid request"}' == \
               resp.content.decode()

    def test_register_long_correct_fields(self):
        context = user_fields.copy()
        context['first_name'] = 't'*255
        context['last_name'] = 'w'*255
        context['organization'] = 'q'*255

        resp = self.client.post(reverse('core_user:register'),
                                convert_to_json(context),
                                content_type="application/json")

        check_registration(resp, context)

    def test_register_long_incorrect_fields(self):
        context = user_fields.copy()
        context['first_name'] = 't'*256
        context['last_name'] = 'w'*256
        context['organization'] = 'q'*256

        resp = self.client.post(reverse('core_user:register'),
                                convert_to_json(context),
                                content_type="application/json")

        assert 400 == resp.status_code
        assert '{"code":400,"message":"invalid request"}' == \
               resp.content.decode()

    def test_register_one_symbol_fields(self):
        context = user_fields.copy()
        context['first_name'] = 't'
        context['last_name'] = 'w'
        context['organization'] = 'q'

        resp = self.client.post(reverse('core_user:register'),
                                convert_to_json(context),
                                content_type="application/json")

        check_registration(resp, context)

    def test_register_empty_fields(self):
        context = user_fields.copy()
        context['first_name'] = ''
        context['last_name'] = ''
        context['organization'] = ''

        resp = self.client.post(reverse('core_user:register'),
                                convert_to_json(context),
                                content_type="application/json")

        assert 400 == resp.status_code
        assert '{"code":400,"message":"invalid request"}' == \
               resp.content.decode()

    def test_register_no_fields(self):
        resp = self.client.post(reverse('core_user:register'), {})

        assert 400 == resp.status_code
        assert '{"code":400,"message":"invalid request"}' == \
               resp.content.decode()

    def test_register_complicated_organisation(self):
        context = user_fields.copy()
        context['organization'] = 'qwert12345@g.organisation----lol'

        resp = self.client.post(reverse('core_user:register'),
                                convert_to_json(context),
                                content_type="application/json")

        check_registration(resp, context)

    def test_register_incorrect_fields(self):
        context = user_fields.copy()
        context['first_name'] = 'qwerty12345'
        context['last_name'] = 'qwerty12345'
        context['organization'] = 'qwerty12345'

        resp = self.client.post(reverse('core_user:register'),
                                convert_to_json(context),
                                content_type="application/json")

        assert 400 == resp.status_code
        assert '{"code":400,"message":"invalid request"}' == \
               resp.content.decode()

    def test_register_incorrect_email(self):
        context = user_fields.copy()
        context['email'] = 'qwerty12345'

        resp = self.client.post(reverse('core_user:register'),
                                convert_to_json(context),
                                content_type="application/json")

        assert 400 == resp.status_code
        assert '{"code":400,"message":"invalid request"}' == \
               resp.content.decode()


class TestSearchView(TestCase):

    ok_status_code = 200
    incorrect_status_code = 400
    incorrect_message = '{"code":400,"message":"invalid request"}'

    @classmethod
    def setUpClass(cls):
        set_links_in_db_from_file('core/tests/links_example.json')

    @classmethod
    def tearDownClass(cls):
        links = Links.objects.all()
        for link in links:
            link.delete()

    def test_url_search_access_by_name(self):
        context = search_link_fields.copy()
        context['doc_id_to'] = -1
        resp = self.client.post(reverse('core:search'),
                                convert_to_json(context),
                                content_type="application/json")
        assert self.ok_status_code == resp.status_code

    def test_url_search_access_by_url(self):
        context = search_link_fields.copy()
        context['doc_id_to'] = -1

        resp = self.client.post('/api/search/get', convert_to_json(context),
                                content_type="application/json")
        assert self.ok_status_code == resp.status_code

    def test_empty_query(self):
        context = {'doc_id_to': -1, 'doc_id_from': -1}

        resp = self.client.post('/api/search/get', convert_to_json(context),
                                content_type="application/json")
        assert self.incorrect_status_code == resp.status_code
        assert self.incorrect_message == resp.content.decode()

