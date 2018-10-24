# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.forms import CustomUserCreationForm, CustomUserChangeForm
from core.models import CustomUser, Links


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'username', 'email',
                    'organization']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Links)
