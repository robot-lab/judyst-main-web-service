from django.test import TestCase

from core.tests.utils import default_user_fields, link_fields
from core.models import CustomUser, Links
from core.utils.functions import create_user_from_fields, \
    create_link_from_fields


# Magic constants take from specification.
class TestUserModel(TestCase):

    text_field_max_length = 255

    @classmethod
    def setUpClass(cls):
        create_user_from_fields(default_user_fields)

    @classmethod
    def tearDownClass(cls):
        users = CustomUser.objects.all()
        for user in users:
            user.delete()

    def test_name(self):
        user = CustomUser.objects.get(email=default_user_fields['email'])
        field_label = user._meta.get_field('first_name').verbose_name
        length = user._meta.get_field('first_name').max_length
        assert 'first name' == field_label
        assert self.text_field_max_length == length
        assert default_user_fields['first_name'] == user.first_name

    def test_surname(self):
        user = CustomUser.objects.get(email=default_user_fields['email'])
        field_label = user._meta.get_field('last_name').verbose_name
        length = user._meta.get_field('last_name').max_length
        assert 'last name' == field_label
        assert self.text_field_max_length == length
        assert default_user_fields['last_name'] == user.last_name

    def test_email(self):
        user = CustomUser.objects.get(email=default_user_fields['email'])
        assert default_user_fields['email'] == user.email

    def test_username(self):
        user = CustomUser.objects.get(email=default_user_fields['email'])
        assert default_user_fields['email'] == user.username

    def test_password(self):
        user = CustomUser.objects.get(email=default_user_fields['email'])
        assert user.check_password(default_user_fields['password'])

    def test_organisation(self):
        user = CustomUser.objects.get(email=default_user_fields['email'])
        organization_label = user._meta.get_field('organization').verbose_name
        max_length = user._meta.get_field('organization').max_length
        assert 'organization' == organization_label
        assert self.text_field_max_length == max_length
        assert default_user_fields['organization'] == user.organization

    def test_verificate(self):
        user = CustomUser.objects.get(email=default_user_fields['email'])
        verificate_label = user._meta.get_field('verificate').verbose_name
        verificate_default = user._meta.get_field('verificate').default
        assert 'verificate' == verificate_label
        assert isinstance(verificate_default, bool) and not verificate_default

    def test_to_string(self):
        user = CustomUser.objects.get(email=default_user_fields['email'])
        assert default_user_fields['email'] == str(user)


class TestLinksModel(TestCase):

    @classmethod
    def setUpClass(cls):
        create_link_from_fields(link_fields)

    @classmethod
    def tearDownClass(cls):
        links = Links.objects.all()
        for link in links:
            link.delete()

    def test_doc_id_from(self):
        link = Links.objects.get(doc_id_to=link_fields['doc_id_to'])
        doc_id_from_label = link._meta.get_field('doc_id_from').verbose_name
        assert 'doc id from' == doc_id_from_label
        assert link_fields['doc_id_from'] == link.doc_id_from

    def test_doc_id_to(self):
        link = Links.objects.get(doc_id_to=link_fields['doc_id_to'])
        doc_id_to_label = link._meta.get_field('doc_id_to').verbose_name
        assert 'doc id to' == doc_id_to_label
        assert link_fields['doc_id_to'] == link.doc_id_to

    def test_to_doc_title(self):
        link = Links.objects.get(doc_id_to=link_fields['doc_id_to'])
        to_doc_title_label = link._meta.get_field('to_doc_title').verbose_name
        assert 'to doc title' == to_doc_title_label
        assert link_fields['to_doc_title'] == link.to_doc_title

    def test_citations_number(self):
        link = Links.objects.get(doc_id_to=link_fields['doc_id_to'])
        citations_number_label = link._meta.get_field('citations_number').\
            verbose_name
        assert 'citations number' == citations_number_label
        assert link_fields['citations_number'] == link.citations_number

    def test_contexts_list(self):
        link = Links.objects.get(doc_id_to=link_fields['doc_id_to'])
        contexts_list_label = link._meta.get_field('contexts_list').\
            verbose_name
        assert 'contexts list' == contexts_list_label
        assert link_fields['contexts_list'] == link.contexts_list

    def test_positions_list(self):
        link = Links.objects.get(doc_id_to=link_fields['doc_id_to'])
        positions_list_label = link._meta.get_field('positions_list').\
            verbose_name
        assert 'positions list' == positions_list_label
        assert link_fields['positions_list'] == link.positions_list
