import pytest

from core.tests.utils import default_user_fields, another_user_fields, \
    link_fields, login_fields, is_equal_lists


@pytest.fixture(scope="function",
                params=[(another_user_fields,),
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
