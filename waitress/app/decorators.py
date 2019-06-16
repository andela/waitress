from app.models import Passphrase
from rest_framework import status as status_code
from rest_framework.response import Response
from functools import wraps


def guard(func):
    """
    This decorator enforces passphrase authentication.
    """
    @wraps(func)
    def decorated_func(viewset, request, pk=None, *args, **kwargs):
        passphrase = request.POST.get('passphrase', None)
        is_user_permitted = ((not request.user.is_anonymous) and (request.user.is_staff))
        exists = Passphrase.exists(passphrase)
        if exists.status or is_user_permitted:
            request.passphrase = exists.matched_list[0] if exists.status else request.user.id
            if pk:
                return func(viewset, request, pk, *args, **kwargs)
            return func(viewset, request, *args, **kwargs)
        else:
            content = {'status': 'Invalid passphrase. Contact the admin to provide authorization'}
            status = status_code.HTTP_401_UNAUTHORIZED
            return Response(content, status=status)

    return decorated_func
