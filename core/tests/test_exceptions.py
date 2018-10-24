from django.test import TestCase

from core.utils.exceptions import ErrorResponse


# Magic constants take from specification.
class TestErrorCode(TestCase):

    invalid_error_code = 400
    invalid_message = "invalid request"
    user_exist_message = "user already exist"

    def test_not_valid_data(self):
        response = ErrorResponse().not_valid()
        assert {"code": self.invalid_error_code,
                "message": self.invalid_message} == response.data

    def test_not_valid_code(self):
        response = ErrorResponse().not_valid()
        assert self.invalid_error_code == response.status_code

    def test_user_exist_data(self):
        response = ErrorResponse().user_exist()
        assert {"code": self.invalid_error_code,
                "message": self.user_exist_message} == response.data

    def test_user_exist_code(self):
        response = ErrorResponse().user_exist()
        assert self.invalid_error_code == response.status_code
