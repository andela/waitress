from functools import wraps

from django.http import JsonResponse


def guard(func):
    """
    This decorator enforces user authentication.
    """

    @wraps(func)
    def decorated_func(viewset, request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(viewset, request, *args, **kwargs)
        else:
            return JsonResponse({ 'message': 'Unauthorized Request' }, status=401)

    return decorated_func
