"""
Test user model.
"""
import pytest

from core.tests.utils import default_user_fields, default_user_in_bd, \
    from_params_to_id, TestConstants
from core.models import CustomUser


@pytest.fixture(scope="function",
                params=[('first_name', 'first name',
                         TestConstants.text_field_max_length),
                        ('last_name', 'last name',
                         TestConstants.text_field_max_length),
                        ('organization', 'organization',
                         TestConstants.text_field_max_length)],
                ids=from_params_to_id
                )
def param_custom_user_fields(request):
    return request.param


@pytest.mark.django_db
def test_user_fields_values(default_user_in_bd):
    user = CustomUser.objects.get(email=default_user_fields['email'])
    assert default_user_fields['first_name'] == user.first_name
    assert default_user_fields['last_name'] == user.last_name
    assert default_user_fields['email'] == user.email
    assert default_user_fields['email'] == user.username
    assert user.check_password(default_user_fields['password'])
    assert default_user_fields['organization'] == user.organization
    assert not user.verification


@pytest.mark.django_db
def test_fields_params(default_user_in_bd, param_custom_user_fields):
    field_name, expected_field_label, expected_max_length = \
        param_custom_user_fields
    user = CustomUser.objects.get(email=default_user_fields['email'])
    actual_field_label = user._meta.get_field(field_name).verbose_name
    actual_max_length = user._meta.get_field(field_name).max_length
    assert expected_field_label == actual_field_label
    assert expected_max_length == actual_max_length


@pytest.mark.django_db
def test_verification(default_user_in_bd):
    user = CustomUser.objects.get(email=default_user_fields['email'])
    verification_label = user._meta.get_field('verification').verbose_name
    verification_default = user._meta.get_field('verification').default
    assert 'verification' == verification_label
    assert isinstance(verification_default, bool) and not verification_default


@pytest.mark.django_db
def test_to_string(default_user_in_bd):
    user = CustomUser.objects.get(email=default_user_fields['email'])
    assert default_user_fields['email'] == str(user)
