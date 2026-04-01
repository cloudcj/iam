# # project/utils/exceptions.py
# from rest_framework.views import exception_handler
# from django.db.models import ProtectedError
# from rest_framework.response import Response
# from rest_framework import status

# def custom_exception_handler(exc, context):
#     if isinstance(exc, ProtectedError):
#         blocked = [str(obj) for obj in exc.protected_objects]
#         return Response(
#             {"detail": f"Cannot delete because of related objects: {', '.join(blocked)}"},
#             status=status.HTTP_400_BAD_REQUEST
#         )
#     return exception_handler(exc, context)

# project/utils/exceptions.py
from rest_framework.views import exception_handler
from django.db.models import ProtectedError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    # Handle FK protected delete
    if isinstance(exc, ProtectedError):
        blocked = [str(obj) for obj in exc.protected_objects]
        return Response(
            {
                "message": f"Cannot delete because of related objects: {', '.join(blocked)}"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    response = exception_handler(exc, context)

    if response is None:
        return response

    # Keep validation errors as-is
    if isinstance(exc, ValidationError):
        return response

    # Replace "detail" → "message"
    if isinstance(response.data, dict) and "detail" in response.data:
        response.data = {
            "message": response.data["detail"]
        }

    return response
