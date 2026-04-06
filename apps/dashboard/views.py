from datetime import timedelta

from django.db.models import Count
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit.models import AuditLog
from apps.authz.permissions import HasPermission
from apps.common.constants.permission_codes import IAMPermissions
from apps.department.models.department import Department
from apps.identity.models.user import User


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = IAMPermissions.AUDIT_READ

    def get(self, request):
        seven_days_ago = now() - timedelta(days=7)

        # --- Stats ---
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        inactive_users = total_users - active_users
        total_departments = Department.objects.count()

        # --- Users by Department ---
        users_by_department = list(
            Department.objects.annotate(user_count=Count("users"))
            .values("name", "user_count")
            .order_by("-user_count")
        )

        # --- Login stats (last 7 days) ---
        failed_logins_7d = AuditLog.objects.filter(
            action=AuditLog.Action.AUTH_LOGIN_FAILED,
            timestamp__gte=seven_days_ago,
        ).count()

        login_success_7d = AuditLog.objects.filter(
            action=AuditLog.Action.AUTH_LOGIN,
            status=AuditLog.Status.SUCCESS,
            timestamp__gte=seven_days_ago,
        ).count()

        # --- Recent Activity (last 10) ---
        recent_logs = (
            AuditLog.objects.select_related("actor", "actor__department")
            .order_by("-timestamp")[:10]
        )
        recent_activity = [
            {
                "id": str(log.id),
                "actor": log.actor.username if log.actor else None,
                "actor_name": f"{log.actor.first_name} {log.actor.last_name}".strip() if log.actor else None,
                "action": log.action,
                "status": log.status,
                "ip_address": log.ip_address,
                "timestamp": log.timestamp.isoformat(),
            }
            for log in recent_logs
        ]

        # --- Top Actors last 7 days (top 5) ---
        top_actors_qs = (
            AuditLog.objects.filter(
                timestamp__gte=seven_days_ago,
                actor__isnull=False,
            )
            .values("actor__username", "actor__first_name", "actor__last_name")
            .annotate(event_count=Count("id"))
            .order_by("-event_count")[:5]
        )
        top_actors = [
            {
                "username": a["actor__username"],
                "name": f"{a['actor__first_name']} {a['actor__last_name']}".strip(),
                "event_count": a["event_count"],
            }
            for a in top_actors_qs
        ]

        # --- Recent Admin Actions (last 10) ---
        admin_action_types = [
            AuditLog.Action.USER_CREATE,
            AuditLog.Action.USER_UPDATE,
            AuditLog.Action.USER_DELETE,
            AuditLog.Action.USER_RESET_PASSWORD,
            AuditLog.Action.DEPT_CREATE,
            AuditLog.Action.DEPT_UPDATE,
            AuditLog.Action.DEPT_DELETE,
        ]
        admin_logs = (
            AuditLog.objects.select_related("actor")
            .filter(action__in=admin_action_types)
            .order_by("-timestamp")[:10]
        )
        recent_admin_actions = [
            {
                "id": str(log.id),
                "actor": log.actor.username if log.actor else None,
                "actor_name": f"{log.actor.first_name} {log.actor.last_name}".strip() if log.actor else None,
                "action": log.action,
                "target_type": log.target_type,
                "status": log.status,
                "timestamp": log.timestamp.isoformat(),
            }
            for log in admin_logs
        ]

        return Response({
            "stats": {
                "total_users": total_users,
                "active_users": active_users,
                "inactive_users": inactive_users,
                "total_departments": total_departments,
            },
            "users_by_department": users_by_department,
            "failed_logins_7d": failed_logins_7d,
            "login_success_7d": login_success_7d,
            "recent_activity": recent_activity,
            "top_actors": top_actors,
            "recent_admin_actions": recent_admin_actions,
        })
