import pytest

from django.urls import reverse

from core.tests.utils import TestConstants, default_user_in_bd_logged_in


@pytest.mark.django_db
def test_url_logout_exist_at_desired_location(client):
    resp = client.get('/api/user/logout')
    assert TestConstants.ok_status_code == resp.status_code


@pytest.mark.django_db
def test_url_logout_access_by_name(client):
    resp = client.get(reverse('core_user:logout'))
    assert TestConstants.ok_status_code == resp.status_code


@pytest.mark.django_db
def test_correct_logout(client, default_user_in_bd_logged_in):
    resp = client.get(reverse('core_user:logout'))
    assert TestConstants.ok_status_code == resp.status_code
