import user_agents
from apps.audit.models import AuditLog


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def get_user_agent_info(request):
    if not request:
        return {}
    ua_string = request.META.get("HTTP_USER_AGENT", "")
    if not ua_string:
        return {}
    ua = user_agents.parse(ua_string)
    return {
        "browser": f"{ua.browser.family} {ua.browser.version_string}",
        "os": f"{ua.os.family} {ua.os.version_string}".strip(),
        "device": "Mobile" if ua.is_mobile else "Tablet" if ua.is_tablet else "Desktop",
    }


def log_action(
    *,
    action,
    actor=None,
    target_id=None,
    target_type="",
    status=AuditLog.Status.SUCCESS,
    detail=None,
    request=None,
    ip_address=None,
):
    merged_detail = {**(detail or {}), **get_user_agent_info(request)}
    AuditLog.objects.create(
        actor=actor,
        action=action,
        target_id=target_id,
        target_type=target_type,
        status=status,
        detail=merged_detail,
        ip_address=ip_address or (get_client_ip(request) if request else None),
    )
