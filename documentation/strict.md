from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

def patch(self, request, user_id):
    try:
        update_user_department(
            user_id=user_id,
            department_code=request.data.get("department"),
        )
    except DjangoValidationError as e:
        raise DRFValidationError(e.message_dict)

    return Response(status=204)
