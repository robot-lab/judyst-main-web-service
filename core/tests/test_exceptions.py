from django.test import TestCase
from core.utils.exceptions import ErrorResponse


class TestErrorCode(TestCase):

    def test_not_valid_data(self):
        response = ErrorResponse().not_valid()
        self.assertEqual(response.data, {"code": 400,
                                         "message": "invalid request"})

    def test_not_valid_code(self):
        response = ErrorResponse().not_valid()
        self.assertEqual(response.status_code, 400)

    def test_user_exist_data(self):
        response = ErrorResponse().user_exist()
        self.assertEqual(response.data, {"code": 400,
                                         "message": "user already exist"})

    def test_user_exist_code(self):
        response = ErrorResponse().user_exist()
        self.assertEqual(response.status_code, 400)
