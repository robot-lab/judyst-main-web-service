"""
Test common functions.
"""
import pytest

from core.utils.functions import is_not_valid_text_fields, \
    is_not_fields_include


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
