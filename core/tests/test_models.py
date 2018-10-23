from django.test import TestCase

from core.models import CustomUser


# Magic constants take from specification.
class TestUserModel(TestCase):

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

    def test_name(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        field_label = user._meta.get_field('first_name').verbose_name
        length = user._meta.get_field('first_name').max_length
        assert 'first name' == field_label
        assert 255 == length
        assert 'name' == user.first_name

    def test_surname(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        field_label = user._meta.get_field('last_name').verbose_name
        length = user._meta.get_field('last_name').max_length
        assert 'last name' == field_label
        assert 255 == length
        assert 'surname' == user.last_name

    def test_email(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        assert 'goodEmail@gmail.com' == user.email

    def test_username(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        assert 'goodEmail@gmail.com' == user.username

    def test_password(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        assert user.check_password('p4thw0rd')

    def test_organisation(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        organization_label = user._meta.get_field('organization').verbose_name
        max_length = user._meta.get_field('organization').max_length
        assert 'organization' == organization_label
        assert 255 == max_length
        assert 'My organisation' == user.organization

    def test_verificate(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        verificate_label = user._meta.get_field('verificate').verbose_name
        verificate_default = user._meta.get_field('verificate').default
        assert 'verificate' == verificate_label
        assert isinstance(verificate_default, bool) and not verificate_default

    def test_to_string(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        assert 'goodEmail@gmail.com' == str(user)
