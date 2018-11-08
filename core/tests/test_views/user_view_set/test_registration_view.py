import pytest

from json import loads, dumps

from django.urls import reverse

from rest_framework.authtoken.models import Token

from core.models import CustomUser, Links
from core.utils.functions import create_user_from_fields
from core.tests.utils import get_dict_from_user, another_user_fields, login_fields, \
    default_user_fields, set_links_in_db_from_file, is_equal_lists, \
    get_dict_from_link, set_links_in_db_from_list, TestConstants, \
    default_user_in_bd, default_user_in_bd_logged_in
from core.tests.test_views.user_view_set.fields_values import \
    param_password_field, param_email_field, param_organization_field, \
    param_text_field


def check_registration(resp, context, mailoutbox):
    """
    Function for checking registration process.

    :param resp: Response
        Response of test client for analysing.

    :param context: dict
        Dict with fields for new user.
    """
    users = CustomUser.objects.filter(username=context['email'])

    # Check tha was added exactly one user.
    assert 1 == len(users)

    user = users[0]

    user_dict = get_dict_from_user(user)
    for field in another_user_fields:
        if field != 'password':
            assert context[field] == user_dict[field]
        else:
            assert user.check_password(context[field])

    expected_token, _ = Token.objects.get_or_create(user=user)

    assert TestConstants.ok_status_code == resp.status_code

    assert '{"token":"' + str(expected_token) + '"}' == \
           resp.content.decode()

    # Check that was added exactly one message.
    assert 1 == len(mailoutbox)

    message = mailoutbox[0]

    # Check that was send to exactly one address.
    assert 1 == len(message.to)
    assert context['email'] == message.to[0]
    assert TestConstants.email_text == message.body


@pytest.mark.django_db
def test_url_register_exist_at_desired_location(client, default_user_in_bd,
                                                mailoutbox):
    context = another_user_fields.copy()
    resp = client.post('/api/user/register', dumps(context),
                       content_type="application/json")
    assert TestConstants.ok_status_code == resp.status_code


@pytest.mark.django_db
def test_url_register_access_by_name(client, default_user_in_bd, mailoutbox):
    context = another_user_fields.copy()
    resp = client.post(reverse('core_user:register'), dumps(context),
                       content_type="application/json")
    assert TestConstants.ok_status_code == resp.status_code


@pytest.mark.django_db
def test_register_no_fields(client, default_user_in_bd, mailoutbox):
    resp = client.post(reverse('core_user:register'), dumps({}),
                       content_type="application/json")
    assert TestConstants.error_status_code == resp.status_code
    assert TestConstants.invalid_request_text == resp.content.decode()


@pytest.mark.django_db
def test_register_already_logged_in(client, default_user_in_bd_logged_in,
                                    mailoutbox):
    context = another_user_fields.copy()
    resp = client.post(reverse('core_user:register'), dumps(context),
                       content_type="application/json")
    check_registration(resp, context, mailoutbox)


@pytest.mark.django_db
def test_register_already_exist(client, default_user_in_bd, mailoutbox):
    context = default_user_fields.copy()
    resp = client.post(reverse('core_user:register'), dumps(context),
                       content_type="application/json")
    assert TestConstants.error_status_code == resp.status_code
    assert TestConstants.user_already_exist_text == resp.content.decode()


@pytest.mark.django_db
def test_register_already_exist_logged_in(client, default_user_in_bd_logged_in,
                                    mailoutbox):
    context = default_user_fields.copy()
    resp = client.post(reverse('core_user:register'), dumps(context),
                       content_type="application/json")
    assert TestConstants.error_status_code == resp.status_code
    assert TestConstants.user_already_exist_text == resp.content.decode()


@pytest.mark.django_db
def test_register_check_correction(client, param_password_field,
                                   param_email_field, param_organization_field,
                                   param_text_field, mailoutbox,
                                   default_user_in_bd):
    password_text, password_correction = param_password_field
    email_text, email_correction = param_email_field
    organization_text, organization_correction = param_organization_field
    text_field, text_correction = param_text_field

    context = {'email': email_text, 'password': password_text,
               'first_name': text_field, 'last_name': text_field,
               'organization': organization_text}
    resp = client.post(reverse('core_user:register'), dumps(context),
                       content_type="application/json")

    if password_correction and email_correction and organization_correction \
        and text_correction:
        check_registration(resp, context, mailoutbox)
    else:
        assert TestConstants.error_status_code == resp.status_code
        assert TestConstants.invalid_request_text == resp.content.decode()
