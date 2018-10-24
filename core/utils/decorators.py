from django.shortcuts import redirect
from rest_framework.authentication import get_authorization_header


def redirect_if_authorize(func):
    """
    decorator to check is user authorized and if it is so
    it redirect user for another page
    :param func: function for decorating
    :return: decorating function
    """
    def wrapper(self, request, *args, **kwargs):
        if 'Token' in get_authorization_header(request).decode():
            return redirect('/')
        result = func(self, request, *args, **kwargs)
        return result

    return wrapper
