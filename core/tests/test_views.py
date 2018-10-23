from django.test import TestCase
from django.urls import reverse
from core.models import CustomUser


class TestNoUser(TestCase):

    def test_list(self):
        resp = self.client.get(reverse('core:list'))

        assert b'[]' == resp.content
        self.assertEqual(200, resp.status_code)


class TestListView(TestCase):
    def test_url_exist_at_desired_location(self):
        resp = self.client.get('/api/user/list')
        self.assertEqual(200, resp.status_code)

    def test_url_access_by_name(self):
        resp = self.client.get(reverse('core:list'))
        self.assertEqual(200, resp.status_code)


class TestViewsWithUsers(TestCase):

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

    def test_list(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        result = '[{"email":"' + user.email + '","first_name":"' + \
                 user.first_name + '","last_name":"' + user.last_name + \
                 '","username":"' + user.username + '","organization":"' + \
                 user.organization + '","id":' + str(user.id) + '}]'

        resp = self.client.get(reverse('core:list'))

        print('-------------------')
        print(resp.content)
        print(result.encode())

        assert result.encode() == resp.content
        self.assertEqual(200, resp.status_code)
