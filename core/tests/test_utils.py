from django.contrib.auth import authenticate
from django.test import TestCase
from rest_framework.authtoken.models import Token

from core.models import CustomUser
from core.utils.exceptions import ErrorResponse
from core.utils.functions import get_token


# Error response code described in the technical specification.
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


class TestFunctions(TestCase):

    @classmethod
    def setUpClass(cls):
        user = CustomUser.objects.create(email='goodEmail@gmail.com',
                                         username='goodEmail@gmail.com',
                                         first_name='name',
                                         last_name='surname',
                                         organization='My organisation')
        user.set_password('p4thw0rd')
        user.save()

    @classmethod
    def tearDownClass(cls):
        users = CustomUser.objects.all()
        for user in users:
            user.delete()

    def test_get_token(self):
        session_user = authenticate(username='goodEmail@gmail.com',
                                    password='p4thw0rd')
        right_token, _ = Token.objects.get_or_create(user=session_user)

        token = get_token('goodEmail@gmail.com', 'p4thw0rd')

        self.assertEqual(right_token, token)
