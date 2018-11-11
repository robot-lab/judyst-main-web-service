"""
Test login view.
"""
import pytest

from json import dumps, loads

from django.urls import reverse

from rest_framework.authtoken.models import Token

from core.models import CustomUser
from core.utils.functions import create_user_from_fields
from core.tests.utils import another_user_fields, login_fields, \
    TestConstants, default_user_in_bd, default_user_in_bd_logged_in
from core.tests.test_views.user_view_set.fields_values import \
    param_email_field, param_password_field


@pytest.mark.django_db
def test_login_empty_db(client):
    context = login_fields.copy()

    resp = client.post(reverse('core_user:login'), dumps(context),
                       content_type="application/json")

    assert TestConstants.error_status_code == resp.status_code
    assert TestConstants.invalid_request_text == resp.content.decode()


@pytest.mark.django_db
def test_url_login_exist_at_desired_location(client, default_user_in_bd):
    context = login_fields.copy()
    resp = client.post('/api/user/login', dumps(context),
                       content_type="application/json")
    assert TestConstants.ok_status_code == resp.status_code


@pytest.mark.django_db
def test_url_login_access_by_name(client, default_user_in_bd):
    context = login_fields.copy()
    resp = client.post(reverse('core_user:login'), dumps(context),
                       content_type="application/json")
    assert TestConstants.ok_status_code == resp.status_code


@pytest.mark.django_db
def test_login_no_fields(client):
    context = {}
    resp = client.post(reverse('core_user:login'), dumps(context),
                       content_type="application/json")

    assert TestConstants.error_status_code == resp.status_code
    assert TestConstants.invalid_request_text == resp.content.decode()


@pytest.mark.django_db
def test_login_fields_check_correction(client, param_email_field,
                                       param_password_field):
    email_text, email_correction = param_email_field
    password_text, password_correction = param_password_field

    user = None
    if email_correction and password_correction:
        user_fields = another_user_fields.copy()
        user_fields['email'] = email_text
        user_fields['password'] = password_text
        user = create_user_from_fields(user_fields)

    context = {'email': email_text, 'password': password_text}

    resp = client.post(reverse('core_user:login'), dumps(context),
                       content_type="application/json")

    if email_correction and password_correction:
        expected_token, _ = Token.objects.get_or_create(user=user)
        assert TestConstants.ok_status_code == resp.status_code
        assert {"token": expected_token} == loads(resp.content.decode())
    else:
        assert TestConstants.error_status_code == resp.status_code
        assert TestConstants.invalid_request_text == resp.content.decode()


@pytest.mark.django_db
def test_login_already_logged_in(client, default_user_in_bd_logged_in):
    context = login_fields.copy()

    resp = client.post(reverse('core_user:login'), dumps(context),
                       content_type="application/json")

    users = CustomUser.objects.filter(username=context['email'])

    # Check tha was added exactly one user.
    assert 1 == len(users)

    user = users[0]
    expected_token, _ = Token.objects.get_or_create(user=user)

    assert TestConstants.ok_status_code == resp.status_code
    assert {"token": expected_token} == loads(resp.content.decode())
