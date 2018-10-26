import pytest

import json

from django.core import mail
from django.contrib.auth import authenticate
from django.test import TestCase

from rest_framework.authtoken.models import Token

from core.tests.utils import get_dict_from_user, user_fields, login_fields, \
    default_user_fields, set_links_in_db_from_file, \
    set_links_in_db_from_list, link_fields, get_dict_from_link, \
    is_equal_lists
from core.models import CustomUser, Links
from core.utils.functions import get_token, is_not_valid_text_fields, \
    send_email, get_user_or_none, CheckText, create_user_from_fields, \
    check_email, create_link_from_fields, is_not_fields_include


class TestGetToken(TestCase):
    @classmethod
    def setUpClass(cls):
        create_user_from_fields(default_user_fields)

    @classmethod
    def tearDownClass(cls):
        users = CustomUser.objects.all()
        for user in users:
            user.delete()

    def test_get_token(self):
        session_user = authenticate(username=default_user_fields['email'],
                                    password=default_user_fields['password'])
        expected_token, _ = Token.objects.get_or_create(user=session_user)

        actual_token = get_token(default_user_fields['email'],
                                 default_user_fields['password'])

        assert expected_token == actual_token


class TestGetUserOrNone(TestCase):
    @classmethod
    def setUpClass(cls):
        create_user_from_fields(default_user_fields)

    @classmethod
    def tearDownClass(cls):
        users = CustomUser.objects.all()
        for user in users:
            user.delete()

    def test_get_user(self):
        actual_user = get_user_or_none(default_user_fields['email'])
        expected_user = CustomUser.objects.get(
            email=default_user_fields['email'])
        assert expected_user == actual_user

    def test_no_user(self):
        actual_user = get_user_or_none(user_fields['email'])
        assert actual_user is None


class TestSendEmail(TestCase):

    email_message = 'qwerty12345'
    email_address = 'goodEmail@gmail.com'

    @classmethod
    def setUpClass(cls):
        mail.outbox.clear()

    @classmethod
    def tearDownClass(cls):
        mail.outbox.clear()

    def test_send_email(self):
        send_email(self.email_message, self.email_address)

        # Check that was added exactly one message.
        assert 1 == len(mail.outbox)

        message = mail.outbox[0]

        # Check that was send to exactly one address.
        assert 1 == len(message.to)
        assert self.email_address == message.to[0]
        assert self.email_message == message.body


class TestGetDictFromUser(TestCase):
    @classmethod
    def setUpClass(cls):
        create_user_from_fields(default_user_fields)

    @classmethod
    def tearDownClass(cls):
        users = CustomUser.objects.all()
        for user in users:
            user.delete()

    def test_get_dict_from_user(self):
        user = CustomUser.objects.get(email=default_user_fields['email'])
        actual_result = get_dict_from_user(user)

        expected_result = {'first_name': user.first_name,
                           'last_name': user.last_name,
                           'email': user.email, 'username': user.username,
                           'id': user.id, 'organization': user.organization}

        assert expected_result == actual_result


class TestCreateUserFromDict(TestCase):
    def tearDown(self):
        users = CustomUser.objects.all()
        for user in users:
            user.delete()

    def test_create_user_from_fields(self):
        actual_user = create_user_from_fields(user_fields)
        users = CustomUser.objects.filter(email=user_fields['email'])

        # Check tha was added exactly one user.
        assert 1 == len(users)

        user = users[0]

        user_dict = get_dict_from_user(user)
        for field in user_fields:
            if field != 'password':
                assert user_fields[field] == user_dict[field]
            else:
                assert user.check_password(user_fields[field])

        assert get_dict_from_user(actual_user) == user_dict


class TestLinksFunctions(TestCase):

    def tearDown(self):
        links = Links.objects.all()
        for link in links:
            link.delete()

    def test_links_insertion_from_file(self):
        num = set_links_in_db_from_file('core/tests/links_example.json')

        # Check that was added exactly 7 links.(links_example.json contains
        # 7 links.)
        assert 7 == num
        assert 7 == len(Links.objects.all())

    def test_links_insertion_from_list(self):
        actual_link = set_links_in_db_from_list([link_fields])

        links = Links.objects.filter(doc_id_to=link_fields['doc_id_to'])

        # Check that was added exactly one link.
        assert 1 == len(links)
        assert 1 == actual_link

        stored_link = links[0]

        expected_fields = link_fields.copy()
        expected_fields['id'] = stored_link.id

        assert expected_fields == get_dict_from_link(stored_link)

    def test_get_dict_from_link(self):
        expected_link = Links.objects.create(
            doc_id_from=link_fields['doc_id_from'],
            doc_id_to=link_fields['doc_id_to'],
            to_doc_title=link_fields['to_doc_title'],
            citations_number=link_fields['citations_number'],
            contexts_list=link_fields['contexts_list'],
            positions_list=link_fields['positions_list'])

        actual_dict = get_dict_from_link(expected_link)

        assert expected_link.doc_id_to == actual_dict['doc_id_to']
        assert expected_link.doc_id_from == actual_dict['doc_id_from']
        assert expected_link.to_doc_title == actual_dict['to_doc_title']
        assert expected_link.citations_number == \
               actual_dict['citations_number']
        assert expected_link.contexts_list == actual_dict['contexts_list']
        assert expected_link.positions_list == actual_dict['positions_list']
        assert expected_link.id == actual_dict['id']

    def test_create_link_from_field(self):
        actual_link = create_link_from_fields(link_fields)

        links = Links.objects.filter(doc_id_to=link_fields['doc_id_to'])

        # Check that was added exactly one link.
        assert 1 == len(links)

        stored_link = links[0]

        expected_fields = link_fields.copy()
        expected_fields['id'] = stored_link.id

        assert expected_fields == get_dict_from_link(actual_link)
        assert expected_fields == get_dict_from_link(stored_link)


@pytest.fixture(scope="function",
                params=[('qwerty1', False),
                        ('qwerty', True)],
                ids=["not latin", "latin"])
def param_is_latin(request):
    return request.param


def test_is_latin(param_is_latin):
    data, result = param_is_latin
    assert result == CheckText.check_line(data)


@pytest.fixture(scope="function",
                params=[({'1': '1'}, ['1'], None, None, False, False),
                        ({'1': ''}, ['1'], None, None, False, True),
                        ({'1': '1'}, ['2'], None, None, False, True),
                        ({'1': '1', '2': '2'}, ['2', '1'], None, None, False,
                         False),
                        ({'1': '1', '2': '2'}, ['2', '3'], None, None, False,
                         True),
                        ({'1': '11', '2': '22'}, ['2', '1'], None, None, False,
                         False),
                        ({'1': '11', '2': '22'}, ['2', '1'], 1, 3, False,
                         False),
                        ({'1': '11', '2': '22'}, ['2', '1'], 3, 5, False,
                         True),
                        ({'1': '11', '2': '22'}, ['2', '1'], None, 1, False,
                         True),
                        ({'1': 'aa', '2': 'bb'}, ['2', '1'], 1, 3, True,
                         False),
                        ({'1': 'aa', '2': 'b2'}, ['2', '1'], None, 3, True,
                         True),
                        ({'1': '111'}, ['1'], None, 3, False, False),
                        ({'1': '111'}, ['1'], None, 2, False, True),
                        ({'1': '111'}, ['1'], 3, None, False, False),
                        ({'1': '111'}, ['1'], 4, None, False, True),
                        ({'1': 1}, ['1'], None, None, False, True)
                        ],
                ids=["check inclusion", "empty field", "without field",
                     "many fields", "not all fields", "other order",
                     "with length checks", "short fields", "long fields",
                     "only latin", "not only latin", "equal up border",
                     "up border +1", "equal down border", "down border -1",
                     "not a string"])
def param_is_not_valid_text_fields(request):
    return request.param


def test_is_not_valid_text_fields(param_is_not_valid_text_fields):
    data, fields, min_length, max_length, only_latin, result = \
        param_is_not_valid_text_fields
    assert result == is_not_valid_text_fields(data, fields,
                                              max_length=max_length,
                                              min_length=min_length,
                                              only_latin=only_latin)


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
                params=[({'1': '11'}, ['1'], False),
                        ({'1': '11'}, ['2'], True),
                        ({'1': '11', '2': '22'}, ['1', '2'], False),
                        ({'1': '11', '2': '22'}, ['1', '3'], True),
                        ({'1': 11, '2': 2.2}, ['1', '2'], False)],
                ids=["correct", "incorrect", "many fields",
                     "many fields incorrect", "not string"])
def param_is_not_fields_include(request):
    return request.param


def test_is_not_fields_include(param_is_not_fields_include):
    data, fields, result = param_is_not_fields_include
    assert result == is_not_fields_include(data, fields)


@pytest.fixture(scope="function",
                params=[(user_fields, ),
                        (default_user_fields, )],
                ids=["user_fields", "default_user_fields"])
def param_user_fields(request):
    return request.param


def test_user_fields(param_user_fields):
    fields = param_user_fields[0]
    assert 'email' in fields
    assert isinstance(fields['email'], str)
    assert 'password' in fields
    assert isinstance(fields['password'], str)
    assert 'first_name' in fields
    assert isinstance(fields['first_name'], str)
    assert 'last_name' in fields
    assert isinstance(fields['last_name'], str)
    assert 'organization' in fields
    assert isinstance(fields['organization'], str)


def test_login_fields():
    assert 'email' in login_fields
    assert isinstance(login_fields['email'], str)
    assert 'password' in login_fields
    assert isinstance(login_fields['password'], str)


def test_link_fields():
    assert 'doc_id_from' in link_fields
    assert isinstance(link_fields['doc_id_from'], str)
    assert 'doc_id_to' in link_fields
    assert isinstance(link_fields['doc_id_to'], str)
    assert 'citations_number' in link_fields
    assert isinstance(link_fields['citations_number'], int)
    assert 'contexts_list' in link_fields
    assert isinstance(link_fields['contexts_list'], list)
    assert 'positions_list' in link_fields
    assert isinstance(link_fields['positions_list'], list)


@pytest.fixture(scope="function", params=[(TypeError, "121", [7])],
                ids=["not list and not string"])
def params_equal_lists_raise(request):
    return request.param


def test_equal_lists_raise(params_equal_lists_raise):
    error, list1, list2 = params_equal_lists_raise
    with pytest.raises(error):
        is_equal_lists(list1, list2)


# Need to test this function on any type of data.
@pytest.fixture(scope="function",
                params=[(["1989"], ['1989'], True),
                        (['1989'], ['1990'], False),
                        (['1989', '1990'], ['1990', '1989'], True),
                        (['1989'], ['1990', '1989'], False),
                        ([], [], True),
                        (['1989', '1989'], ['1990'], False),
                        (['1989', '1990'], ['1989', '1990'], True),
                        (['1989', '1989'], ['1989', '1989'], True),
                        (['1989', '1990'], ['1989', '1990', '1989'], False),
                        ([12, 1], [1, 12], True),
                        ([{}, {}], [{}, {}, {}], False)],
                ids=["same list one element", 'different element',
                     'different order', 'first smaller than second',
                     'empty lists', 'first bigger than second',
                     'same list many elements', 'same list with repetitions',
                     'equal after deleting repetitions', 'not string',
                     'different number of empty dictionaries'])
def params_equal_lists(request):
    return request.param


def test_equal_lists(params_equal_lists):
    list1, list2, result = params_equal_lists
    assert result == is_equal_lists(list1, list2)


def test_used_production_db():
    with open('conf.json', 'r') as f_in:
        conf = json.load(f_in)
        assert conf['host'] == "68.183.66.108"
