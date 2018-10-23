from django.test import TestCase

from core.utils.exceptions import ErrorResponse


# Magic constants take from specification.
class TestErrorCode(TestCase):

    def test_not_valid_data(self):
        response = ErrorResponse().not_valid()
        assert {"code": 400, "message": "invalid request"} == response.data

    def test_not_valid_code(self):
        response = ErrorResponse().not_valid()
        assert 400 == response.status_code

    def test_user_exist_data(self):
        response = ErrorResponse().user_exist()
        assert {"code": 400, "message": "user already exist"} == response.data

    def test_user_exist_code(self):
        response = ErrorResponse().user_exist()
        assert 400 == response.status_code
