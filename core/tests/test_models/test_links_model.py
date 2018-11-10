from django.test import TestCase

from core.tests.utils import link_fields
from core.models import Links
from core.utils.functions import create_link_from_fields


# Magic constants take from specification.
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
