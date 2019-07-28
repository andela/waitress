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
            return JsonResponse({"message": "Unauthorized Request"}, status=401)

    return decorated_func


def validateHttpMethod(func):
    """
    This method is used to validate the http
    method received by the different django views
    """

    @wraps(func)
    def decorated_func(request, *args, **kwargs):
        # if request.user.is_authenticated:
        return func(request, *args, **kwargs)

    return decorated_func
