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
        self.assertEqual(field_label, 'first name')
        length = user._meta.get_field('first_name').max_length
        self.assertEqual(length, 255)
        self.assertEqual('name', user.first_name)

    def test_surname(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        field_label = user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')
        length = user._meta.get_field('last_name').max_length
        self.assertEqual(length, 255)
        self.assertEqual('surname', user.last_name)

    def test_email(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        self.assertEqual(user.email, 'goodEmail@gmail.com')

    def test_username(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        self.assertEqual(user.username, 'goodEmail@gmail.com')

    def test_password(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        self.assertTrue(user.check_password('p4thw0rd'))

    def test_organisation(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        organization_label = user._meta.get_field('organization').verbose_name
        self.assertEqual(organization_label, 'organization')
        max_length = user._meta.get_field('organization').max_length
        self.assertEqual(max_length, 1024)
        self.assertEqual(user.organization, 'My organisation')

    def test_verificate(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        verificate_label = user._meta.get_field('verificate').verbose_name
        self.assertEqual(verificate_label, 'verificate')
        verificate_default = user._meta.get_field('verificate').default
        self.assertEqual(verificate_default, False)

    def test_to_string(self):
        user = CustomUser.objects.get(email='goodEmail@gmail.com')
        self.assertEqual('goodEmail@gmail.com', str(user))
