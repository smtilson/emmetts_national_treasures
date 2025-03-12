from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    # Handle permission denied for completely unauthenticated requests
    if isinstance(exc, PermissionDenied):
        print("hit permission denied block")
        request = context.get("request")
        if request:
            # Check if the request contains any authentication attempts
            auth_header = request.META.get("HTTP_AUTHORIZATION", "")
            print("auth header: ", auth_header)
            # No auth header provided at all - this is a 401 case
            if not auth_header:
                response.status_code = status.HTTP_401_UNAUTHORIZED
                response.data = {
                    "detail": "Authentication credentials were not provided."
                }

            # Otherwise keep it as 403 - authenticated but insufficient permissions

    # Remap AuthenticationFailed to 401

    if isinstance(exc, AuthenticationFailed):
        response.status_code = status.HTTP_401_UNAUTHORIZED

    return response
