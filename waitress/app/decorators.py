from functools import wraps

from rest_framework import status as status_code
from rest_framework.response import Response

from app.models import Passphrase


def guard(func):
    """
    This decorator enforces passphrase authentication.
    """

    @wraps(func)
    def decorated_func(viewset, request, pk=None, *args, **kwargs):
        passphrase = request.POST.get("passphrase", None)
        exists = Passphrase.exists(passphrase)
        if exists.status:
            request.passphrase = exists.matched_list[0]
            if pk:
                return func(viewset, request, pk, *args, **kwargs)
            return func(viewset, request, *args, **kwargs)
        else:
            content = {
                "status": "Invalid passphrase. Contact the admin to provide authorization"
            }
            status = status_code.HTTP_401_UNAUTHORIZED
            return Response(content, status=status)

    return decorated_func
