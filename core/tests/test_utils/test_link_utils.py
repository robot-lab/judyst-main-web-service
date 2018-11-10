"""
Test functions connected to link model.
"""
from django.test import TestCase

from core.tests.utils import set_links_in_db_from_file, \
    set_links_in_db_from_list, link_fields, get_dict_from_link
from core.models import Links
from core.utils.functions import create_link_from_fields
import pytest

class TestLinksFunctions(TestCase):

    def tearDown(self):
        links = Links.objects.all()
        for link in links:
            link.delete()

    @pytest.mark.skip
    def test_links_insertion_from_file(self):
        num = set_links_in_db_from_file('core/tests/links_example.json')

        # Check that was added exactly 7 links.(links_example.json contains
        # 7 links.)
        assert 7 == num
        assert 7 == len(Links.objects.all())

    @pytest.mark.skip
    def test_links_insertion_from_list(self):
        actual_link = set_links_in_db_from_list([link_fields])

        links = Links.objects.filter(doc_id_to=link_fields['doc_id_to'])

        # Check that was added exactly one link.
        assert 1 == len(links)
        assert 1 == actual_link

        stored_link = links[0]

        expected_fields = link_fields.copy()
        expected_fields['id'] = stored_link.id

        assert expected_fields == get_dict_from_link(stored_link)

    @pytest.mark.skip
    def test_get_dict_from_link(self):
        expected_link = Links.objects.create(
            doc_id_from=link_fields['doc_id_from'],
            doc_id_to=link_fields['doc_id_to'],
            to_doc_title=link_fields['to_doc_title'],
            citations_number=link_fields['citations_number'],
            contexts_list=link_fields['contexts_list'],
            positions_list=link_fields['positions_list'])

        actual_dict = get_dict_from_link(expected_link)

        assert expected_link.doc_id_to == actual_dict['doc_id_to']
        assert expected_link.doc_id_from == actual_dict['doc_id_from']
        assert expected_link.to_doc_title == actual_dict['to_doc_title']
        assert expected_link.citations_number == \
               actual_dict['citations_number']
        assert expected_link.contexts_list == actual_dict['contexts_list']
        assert expected_link.positions_list == actual_dict['positions_list']
        assert expected_link.id == actual_dict['id']

    @pytest.mark.skip
    def test_create_link_from_field(self):
        actual_link = create_link_from_fields(link_fields)

        links = Links.objects.filter(doc_id_to=link_fields['doc_id_to'])

        # Check that was added exactly one link.
        assert 1 == len(links)

        stored_link = links[0]

        expected_fields = link_fields.copy()
        expected_fields['id'] = stored_link.id

        assert expected_fields == get_dict_from_link(actual_link)
        assert expected_fields == get_dict_from_link(stored_link)
