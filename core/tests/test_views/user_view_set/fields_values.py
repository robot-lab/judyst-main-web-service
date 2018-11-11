"""
Fixtures with different values for fields.
Need to test views with given fields values for checking correction of working.
"""
import pytest

from core.tests.utils import TestConstants


@pytest.fixture(scope="function",
                params=[('qwerty', True),
                        ('', False),
                        ('q', True),
                        ('q' * TestConstants.text_field_max_length, True),
                        ('q' * (TestConstants.text_field_max_length+1), False),
                        ('qwerty123', False),
                        ('йцукен', False)],
                ids=["correct", "empty", "one letter", "up border",
                     "up border +1", "with digit", "russian text"])
def param_text_field(request):
    return request.param


@pytest.fixture(scope="function",
                params=[('qwerty@gmail.com', True),
                        ('', False),
                        ('q@t.ui', True),
                        ('q' * (TestConstants.email_field_max_length-10) +
                         '@gmail.com', True),
                        ('q' * (TestConstants.email_field_max_length-9) +
                         '@gmail.com', False),
                        ('qwerty#', False),
                        ('qwert`~!@#)(y@gmail.com', False),
                        ('йцукен@gmail.com', False)],
                ids=["correct", "empty", "small email", "up border",
                     "up border +1", "incorrect structure", "incorrect symbol",
                     "russian text"])
def param_email_field(request):
    return request.param


@pytest.fixture(scope="function",
                params=[('qwerty', True),
                        ('', False),
                        ('q', True),
                        ('q' * TestConstants.text_field_max_length, True),
                        ('q' * (TestConstants.text_field_max_length+1), False),
                        ('qwert12345@g.organisation----lol', True),
                        ('йцукен', True)],
                ids=["correct", "empty", "one letter", "up border",
                     "up border +1", "with special symbols", "russian text"])
def param_organization_field(request):
    return request.param


@pytest.fixture(scope="function",
                params=[('p4thw3450rd', True),
                        ('', False),
                        ('1234567', False),
                        ('12345678', True),
                        ('1' * TestConstants.password_max_size, True),
                        ('0' * (TestConstants.password_max_size+1), False),
                        ('password!', False),
                        ('пароль', False)],
                ids=["correct", "empty field", "down border -1", "down border",
                     "up border", "up border +1", "with special symbols",
                     "russian text"])
def param_password_field(request):
    return request.param
