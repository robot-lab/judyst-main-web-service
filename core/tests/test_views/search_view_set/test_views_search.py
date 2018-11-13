"""
This is unsupported legacy code.
Would be supported lately.
"""
from json import loads, dumps

from django.test import TestCase
from django.urls import reverse

from core.models import Links
from core.tests.utils import set_links_in_db_from_file, is_equal_lists, \
    get_dict_from_link, set_links_in_db_from_list
import pytest

class TestSearchView(TestCase):

    ok_status_code = 200
    incorrect_status_code = 400
    invalid_request_text = '{"code":400,"message":"invalid request"}'
    erase_message = -1

    @classmethod
    def setUpClass(cls):
        set_links_in_db_from_file('core/tests/links_example.json')
        links = Links.objects.all()
        cls.links = [get_dict_from_link(link) for link in links]

    @classmethod
    def tearDownClass(cls):
        links = Links.objects.all()
        for link in links:
            link.delete()

    @pytest.mark.skip
    def test_url_search_access_by_name(self):
        context = {'doc_id_to': self.erase_message,
                   'doc_id_from': self.links[0]['doc_id_from']}

        resp = self.client.post(reverse('core:search'), dumps(context),
                                content_type="application/json")
        assert self.ok_status_code == resp.status_code

    @pytest.mark.skip
    def test_url_search_access_by_url(self):
        context = {'doc_id_to': self.erase_message,
                   'doc_id_from': self.links[0]['doc_id_from']}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")
        assert self.ok_status_code == resp.status_code

    @pytest.mark.skip
    def test_empty_query(self):
        context = {'doc_id_to': self.erase_message,
                   'doc_id_from': self.erase_message}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")
        assert self.incorrect_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    @pytest.mark.skip
    def test_search_all_links(self):
        context = {'doc_id_to': self.erase_message,
                   'doc_id_from': self.links[0]['doc_id_from']}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")

        assert self.ok_status_code == resp.status_code
        assert is_equal_lists(self.links, loads(resp.content.decode()))

    @pytest.mark.skip
    def test_search_no_links_found(self):
        context = {'doc_id_to': self.erase_message,
                   'doc_id_from': "no such file"}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")

        assert self.incorrect_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    @pytest.mark.skip
    def test_search_one_link_one_field_doc_id_to(self):
        # Random number from 0 - 6.
        link_number = 0

        context = {'doc_id_to': self.links[link_number]['doc_id_to'],
                   'doc_id_from': self.erase_message}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")

        assert self.ok_status_code == resp.status_code
        assert is_equal_lists(self.links[link_number:link_number + 1],
                              loads(resp.content.decode()))

    @pytest.mark.skip
    def test_search_one_link_two_field(self):
        # Random number from 0 - 6.
        link_number = 1
        context = {'doc_id_to': self.links[link_number]['doc_id_to'],
                   'doc_id_from': self.links[link_number]['doc_id_from']}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")

        assert self.ok_status_code == resp.status_code
        assert is_equal_lists(self.links[link_number:link_number + 1],
                              loads(resp.content.decode()))

    @pytest.mark.skip
    def test_search_not_link(self):
        context = {'doc_id_to': 'it is not a link',
                   'doc_id_from': 'it is not a link, too'}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")

        assert self.incorrect_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    @pytest.mark.skip
    def test_search_empty_fields(self):
        context = {'doc_id_to': '', 'doc_id_from': ''}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")

        assert self.incorrect_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    @pytest.mark.skip
    def test_search_no_fields(self):
        resp = self.client.post('/api/search/get', dumps({}),
                                content_type="application/json")

        assert self.incorrect_status_code == resp.status_code
        assert self.invalid_request_text == resp.content.decode()

    @pytest.mark.skip
    def test_search_one_link_one_field_doc_id_from(self):
        # Random number from 0 - 6.
        link_number = 1
        link_fields = self.links[link_number].copy()
        link_fields['doc_id_to'], link_fields['doc_id_from'] = \
            link_fields['doc_id_from'], link_fields['doc_id_to']

        set_links_in_db_from_list([link_fields])

        context = {'doc_id_to': self.erase_message,
                   'doc_id_from': link_fields['doc_id_from']}

        resp = self.client.post('/api/search/get', dumps(context),
                                content_type="application/json")

        link = Links.objects.get(doc_id_from=link_fields['doc_id_from'])
        link_fields['id'] = link.id
        link.delete()

        assert self.ok_status_code == resp.status_code
        assert is_equal_lists([link_fields], loads(resp.content.decode()))
