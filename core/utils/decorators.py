from django.shortcuts import redirect
from rest_framework.authentication import get_authorization_header


def redirect_if_authorize(func):
    def wrapper(self, request, *args, **kwargs):
        if 'Token' in get_authorization_header(request).decode():
            return redirect('/')
        result = func(self, request, *args, **kwargs)
        return result

    return wrapper
