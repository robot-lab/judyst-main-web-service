from json import loads, dumps, load

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from rest_framework.authtoken.models import Token

from core.models import CustomUser, Links
from core.utils.functions import create_user_from_fields
from core.tests.utils import get_dict_from_user, user_fields, login_fields, \
    default_user_fields, set_links_in_db_from_file, is_equal_lists, \
    get_dict_from_link, set_links_in_db_from_list


class TestNoUser(TestCase):

    empty_list = '[]'
    ok_status_code = 200
    error_status_code = 400
    invalid_request_text = '{"code":400,"message":"invalid request"}'

    def test_list(self):
        resp = self.client.get(reverse('core_user:list'))

        assert self.empty_list == resp.content.decode()
        assert self.ok_status_code == resp.status_code

    def test_login_no_user(self):
        context = login_fields.copy()

        resp = self.client.post(reverse('core_user:login'), dumps(context),
                                content_type="application/json")

        assert self.error_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()


class TestExistUsers(TestCase):

    email_text = 'Not Implemented:  500'
    ok_status_code = 200
    error_status_code = 400
    user_already_exist_text = '{"code":400,"message":"user already exist"}'
    invalid_request_text = '{"code":400,"message":"invalid request"}'
    text_field_max_length = 255
    email_field_max_length = 150

    def check_registration(self, resp, context):
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

        assert self.ok_status_code == resp.status_code

        assert '{"token":"' + str(expected_token) + '"}' == \
               resp.content.decode()

        assert 1 == len(mail.outbox)

        message = mail.outbox[0]

        assert self.email_text == message.body
        assert 1 == len(message.to)
        assert context['email'] == message.to[0]

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
        assert self.ok_status_code == resp.status_code

    def test_url_list_access_by_name(self):
        resp = self.client.get(reverse('core_user:list'))
        assert self.ok_status_code == resp.status_code

    def test_url_logout_exist_at_desired_location(self):
        resp = self.client.get('/api/user/logout')
        assert self.ok_status_code == resp.status_code

    def test_url_logout_access_by_name(self):
        resp = self.client.get(reverse('core_user:logout'))
        assert self.ok_status_code == resp.status_code

    def test_url_register_exist_at_desired_location(self):
        context = user_fields.copy()
        resp = self.client.post('/api/user/register', dumps(context),
                                content_type="application/json")
        assert self.ok_status_code == resp.status_code

    def test_url_register_access_by_name(self):
        context = user_fields.copy()
        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")
        assert self.ok_status_code == resp.status_code

    def test_url_login_exist_at_desired_location(self):
        context = login_fields.copy()
        resp = self.client.post('/api/user/login', dumps(context),
                                content_type="application/json")
        assert self.ok_status_code == resp.status_code

    def test_url_login_access_by_name(self):
        context = login_fields.copy()
        resp = self.client.post(reverse('core_user:login'), dumps(context),
                                content_type="application/json")
        assert self.ok_status_code == resp.status_code

    def test_list(self):
        users = CustomUser.objects.all()
        expected = [get_dict_from_user(user) for user in users]

        resp = self.client.get(reverse('core_user:list'))
        actual = loads(resp.content.decode())

        assert expected == actual
        assert self.ok_status_code == resp.status_code

    def test_correct_registration(self):
        context = user_fields.copy()

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        self.check_registration(resp, context)

    def test_registration_with_used_email(self):
        context = user_fields.copy()
        context['email'] = default_user_fields['email']

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        assert not mail.outbox

        assert self.error_status_code == resp.status_code
        assert self.user_already_exist_text == resp.content.decode()

    def test_login_correct(self):
        context = login_fields.copy()

        resp = self.client.post(reverse('core_user:login'), dumps(context),
                                content_type="application/json")

        users = CustomUser.objects.filter(username=context['email'])

        assert 1 == len(users)

        user = users[0]
        expected_token, _ = Token.objects.get_or_create(user=user)

        assert self.ok_status_code == resp.status_code
        assert '{"token":"' + str(expected_token) + '"}' == \
               resp.content.decode()

    def test_login_no_fields(self):
        resp = self.client.post(reverse('core_user:login'), dumps({}),
                                content_type="application/json")

        assert self.error_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_login_empty_fields(self):
        resp = self.client.post(reverse('core_user:login'),
                                dumps({'email': '', 'password': ''}),
                                content_type="application/json")

        assert self.error_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_register_long_correct_fields(self):
        context = user_fields.copy()
        context['first_name'] = 't'*self.text_field_max_length
        context['last_name'] = 'w'*self.text_field_max_length
        context['organization'] = 'q'*self.text_field_max_length

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        self.check_registration(resp, context)

    def test_register_long_incorrect_fields(self):
        context = user_fields.copy()
        context['first_name'] = 't'*(self.text_field_max_length+1)
        context['last_name'] = 'w'*(self.text_field_max_length+1)
        context['organization'] = 'q'*(self.text_field_max_length+1)

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        assert self.error_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_register_one_symbol_fields(self):
        context = user_fields.copy()
        context['first_name'] = 't'
        context['last_name'] = 'w'
        context['organization'] = 'q'

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        self.check_registration(resp, context)

    def test_register_empty_fields(self):
        context = user_fields.copy()
        context['first_name'] = ''
        context['last_name'] = ''
        context['organization'] = ''

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        assert self.error_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_register_no_fields(self):
        resp = self.client.post(reverse('core_user:register'), {})

        assert self.error_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_register_complicated_organisation(self):
        context = user_fields.copy()
        context['organization'] = 'qwert12345@g.organisation----lol'

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        self.check_registration(resp, context)

    def test_register_incorrect_fields(self):
        context = user_fields.copy()
        context['first_name'] = 'qwerty12345'
        context['last_name'] = 'qwerty12345'
        context['organization'] = 'qwerty12345'

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        assert self.error_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_register_incorrect_email(self):
        context = user_fields.copy()
        context['email'] = 'qwerty12345'

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        assert self.error_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_register_incorrect_email_dns_name(self):
        context = user_fields.copy()
        context['email'] = 'qwerty12345@mi:mail.com'

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        assert self.error_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_register_email_max_length(self):
        context = user_fields.copy()
        context['email'] = 'q'*(self.email_field_max_length-10) + '@gmail.com'

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        self.check_registration(resp, context)

    def test_register_email_more_than_max_length(self):
        context = user_fields.copy()
        context['email'] = 'q'*(self.email_field_max_length-9) + '@gmail.com'

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        assert self.error_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_empty_password(self):
        context = user_fields.copy()
        context['password'] = ''

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        assert self.error_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_too_short_password(self):
        context = user_fields.copy()
        context['password'] = '1234567'

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        assert self.error_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_short_password(self):
        context = user_fields.copy()
        context['password'] = '12345678'

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        self.check_registration(resp, context)

    def test_long_password(self):
        context = user_fields.copy()
        context['password'] = '1'*64

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        self.check_registration(resp, context)

    def test_too_long_password(self):
        context = user_fields.copy()
        context['password'] = '0'*65

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        assert self.error_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_password_incorrect_characters(self):
        context = user_fields.copy()
        context['password'] = 'password!'

        resp = self.client.post(reverse('core_user:register'), dumps(context),
                                content_type="application/json")

        assert self.error_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()


class TestSearchView(TestCase):

    ok_status_code = 200
    incorrect_status_code = 400
    invalid_request_text = '{"code":400,"message":"invalid request"}'

    @classmethod
    def setUpClass(cls):
        set_links_in_db_from_file('core/tests/links_example.json')
        links = Links.objects.all()
        cls.links = [get_dict_from_link(link) for link in links]

    @classmethod
    def tearDownClass(cls):
        links = Links.objects.all()
        for link in links:
            link.delete()

    def test_url_search_access_by_name(self):
        context = {'doc_id_to': -1,
                   'doc_id_from': self.links[0]['doc_id_from']}

        resp = self.client.post(reverse('core:search'), dumps(context),
                                content_type="application/json")
        assert self.ok_status_code == resp.status_code

    def test_url_search_access_by_url(self):
        context = {'doc_id_to': -1,
                   'doc_id_from': self.links[0]['doc_id_from']}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")
        assert self.ok_status_code == resp.status_code

    def test_empty_query(self):
        context = {'doc_id_to': -1, 'doc_id_from': -1}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")
        assert self.incorrect_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_search_all_links(self):
        context = {'doc_id_to': -1,
                   'doc_id_from': self.links[0]['doc_id_from']}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")

        assert self.ok_status_code == resp.status_code
        assert is_equal_lists(self.links, loads(resp.content.decode()))

    def test_search_no_links_found(self):
        context = {'doc_id_to': -1, 'doc_id_from': "no such file"}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")

        assert self.incorrect_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_search_one_link_one_field_doc_id_to(self):
        context = {'doc_id_to': self.links[0]['doc_id_to'],
                   'doc_id_from': -1}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")

        assert self.ok_status_code == resp.status_code
        assert is_equal_lists(self.links[0:1], loads(resp.content.decode()))

    def test_search_one_link_two_field(self):
        context = {'doc_id_to': self.links[1]['doc_id_to'],
                   'doc_id_from': self.links[1]['doc_id_from']}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")

        assert self.ok_status_code == resp.status_code
        assert is_equal_lists(self.links[1:2], loads(resp.content.decode()))

    def test_search_not_link(self):
        context = {'doc_id_to': 'it is not a link',
                   'doc_id_from': 'it is not a link, too'}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")

        assert self.incorrect_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_search_empty_fields(self):
        context = {'doc_id_to': '', 'doc_id_from': ''}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")

        assert self.incorrect_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_search_no_fields(self):
        resp = self.client.post('/api/search/get', dumps({}),
                                content_type="application/json")

        assert self.incorrect_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    def test_search_one_link_one_field_doc_id_from(self):
        link_fields = self.links[0].copy()
        link_fields['doc_id_to'], link_fields['doc_id_from'] = \
            link_fields['doc_id_from'], link_fields['doc_id_to']

        set_links_in_db_from_list([link_fields])

        context = {'doc_id_to': -1,
                   'doc_id_from': link_fields['doc_id_from']}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")

        link = Links.objects.get(doc_id_from=link_fields['doc_id_from'])
        link_fields['id'] = link.id
        link.delete()

        assert self.ok_status_code == resp.status_code
        assert is_equal_lists([link_fields], loads(resp.content.decode()))
