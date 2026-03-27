from apps.audit.services.services import log_action
from apps.audit.models import AuditLog


class AuditMixin:
    audit_action = None
    audit_target_type = ""

    def get_audit_target_id(self, request, response):
        return None

    def get_audit_detail(self, request, response):
        return {}

    def finalize_response(self, request, response, *args, **kwargs):
        resp = super().finalize_response(request, response, *args, **kwargs)
        if self.audit_action:
            log_action(
                actor=request.user if request.user.is_authenticated else None,
                action=self.audit_action,
                target_id=self.get_audit_target_id(request, resp),
                target_type=self.audit_target_type,
                status=AuditLog.Status.SUCCESS if resp.status_code < 400 else AuditLog.Status.FAILURE,
                detail=self.get_audit_detail(request, resp),
                request=request,
            )
        return resp
