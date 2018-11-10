import pytest

from json import loads

from django.urls import reverse

from core.models import CustomUser
from core.tests.utils import get_dict_from_user, TestConstants, \
    default_user_in_bd, default_user_in_bd_logged_in


@pytest.mark.django_db
def test_url_list_exist_at_desired_location(client):
    resp = client.get('/api/user/list')
    assert TestConstants.ok_status_code == resp.status_code


@pytest.mark.django_db
def test_url_list_access_by_name(client):
    resp = client.get(reverse('core_user:list'))
    assert TestConstants.ok_status_code == resp.status_code


@pytest.mark.django_db
def test_list_with_user_in_db(client, default_user_in_bd):
    users = CustomUser.objects.all()
    expected = [get_dict_from_user(user) for user in users]

    resp = client.get(reverse('core_user:list'))
    actual = loads(resp.content.decode())

    assert expected == actual
    assert TestConstants.ok_status_code == resp.status_code


@pytest.mark.django_db
def test_list_with_user_in_db_logged_in(client, default_user_in_bd_logged_in):
    users = CustomUser.objects.all()
    expected = [get_dict_from_user(user) for user in users]

    resp = client.get(reverse('core_user:list'))
    actual = loads(resp.content.decode())

    assert expected == actual
    assert TestConstants.ok_status_code == resp.status_code


@pytest.mark.django_db
def test_list_with_empty_db(client):
    resp = client.get(reverse('core_user:list'))

    # check that empty list was returned
    assert '[]' == resp.content.decode()
    assert TestConstants.ok_status_code == resp.status_code
