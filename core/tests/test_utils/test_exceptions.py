"""
Test for error response generator
"""

from core.tests.utils import TestConstants
from core.utils.exceptions import ErrorResponse


def test_not_valid():
    response = ErrorResponse().not_valid()
    assert TestConstants.error_status_code == response.status_code
    assert {"code": TestConstants.error_status_code,
            "message": TestConstants.invalid_message} == response.data


def test_user_exist():
    response = ErrorResponse().user_exist()
    assert TestConstants.error_status_code == response.status_code
    assert {"code": TestConstants.error_status_code,
            "message": TestConstants.user_exist_message} == \
           response.data
