from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.audit.models import AuditLog
from apps.authz.permissions import HasPermission
from apps.common.constants.permission_codes import IAMPermissions
from apps.common.pagination import CustomPagination


class AuditLogListView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = IAMPermissions.AUDIT_READ

    def get(self, request):
        qs = AuditLog.objects.select_related("actor", "actor__department").all()

        # filters
        action = request.query_params.get("action")
        status = request.query_params.get("status")
        actor_id = request.query_params.get("actor_id")
        target_type = request.query_params.get("target_type")
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        action_category = request.query_params.get("action_category")
        if action_category == "auth":
            qs = qs.filter(action__startswith="auth.")
        elif action_category == "activity":
            qs = qs.exclude(action__startswith="auth.")

        if action:
            qs = qs.filter(action=action)
        if status:
            qs = qs.filter(status=status)
        if actor_id:
            qs = qs.filter(actor_id=actor_id)
        if target_type:
            qs = qs.filter(target_type=target_type)
        if date_from:
            qs = qs.filter(timestamp__date__gte=date_from)
        if date_to:
            qs = qs.filter(timestamp__date__lte=date_to)

        paginator = CustomPagination()
        page = paginator.paginate_queryset(qs, request)

        data = [
            {
                "id": str(log.id),
                "actor": log.actor.username if log.actor else None,
                "actor_name": f"{log.actor.first_name} {log.actor.last_name}".strip() if log.actor else None,
                "department": log.actor.department.name if log.actor and log.actor.department else None,
                "action": log.action,
                "target_id": str(log.target_id) if log.target_id else None,
                "target_type": log.target_type,
                "status": log.status,
                "detail": log.detail,
                "ip_address": log.ip_address,
                "timestamp": log.timestamp.isoformat(),
            }
            for log in page
        ]

        return paginator.get_paginated_response(data)
