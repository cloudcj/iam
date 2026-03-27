# IAM Audit Logging

## Overview

The audit log records every significant action performed in the IAM system — who did it, what they did, what was affected, and whether it succeeded or failed. It is stored in the database (`iam_audit_log`) so it can be queried and displayed in the UI.

---

## Model: `AuditLog` (`apps/audit/models.py`)

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `actor` | FK → User (nullable) | Who performed the action. `null` for anonymous actions (e.g. failed login with unknown username) |
| `action` | CharField (choices) | What happened. Uses `AuditLog.Action` choices to prevent typos |
| `target_id` | UUID (nullable) | UUID of the affected object (user, department, etc.) |
| `target_type` | CharField | Type of affected object: `"user"`, `"department"` |
| `status` | CharField (choices) | `"success"` or `"failure"` |
| `detail` | JSONField | Extra context — IP address, old/new values, error reasons, etc. |
| `ip_address` | GenericIPAddressField | Client IP, important for auth events |
| `timestamp` | DateTimeField | When the event occurred (auto-set, indexed) |

---

## Action Choices (`AuditLog.Action`)

### Authentication
| Code | Event |
|---|---|
| `auth.login` | Successful login |
| `auth.login_failed` | Failed login attempt |
| `auth.logout` | User logged out |
| `auth.token_refresh` | JWT access token refreshed |

### User Management
| Code | Event |
|---|---|
| `user.create` | New user created |
| `user.update` | User record updated |
| `user.delete` | User deleted |
| `user.reset_password` | Admin reset a user's password |
| `user.change_password` | User changed their own password |

### Department
| Code | Event |
|---|---|
| `dept.create` | Department created |
| `dept.update` | Department updated |
| `dept.delete` | Department deleted |

---

## Status Values

| Value | Meaning |
|---|---|
| `success` | Action completed successfully |
| `failure` | Action was attempted but failed (validation error, permission denied, etc.) |

---

## `detail` JSON Field

The `detail` field stores any extra context that doesn't fit in the fixed columns. Contents vary by action:

### `auth.login` (success)
```json
{ "username": "jdoe" }
```

### `auth.login_failed`
```json
{ "username": "jdoe", "reason": "Invalid credentials" }
```

### `user.create`
```json
{ "username": "jsmith", "department": "Engineering" }
```

### `user.update`
```json
{
  "changed": {
    "first_name": ["John", "Jonathan"],
    "email": ["old@example.com", "new@example.com"]
  }
}
```

### `user.reset_password`
```json
{ "target": "jsmith", "reset_by": "admin" }
```

### `dept.create` / `dept.update` / `dept.delete`
```json
{ "name": "Engineering", "code": "ENGINEERING" }
```

---

## Helper Function

All views use `log_action()` from `apps/audit/services.py` — never write to `AuditLog` directly.

```python
from apps.audit.services import log_action
from apps.audit.models import AuditLog

log_action(
    actor=request.user,             # User instance or None
    action=AuditLog.Action.AUTH_LOGIN,
    target_id=user.id,              # optional
    target_type="user",             # optional
    status=AuditLog.Status.SUCCESS,
    detail={"username": user.username},
    request=request,                # used to extract ip_address
)
```

---

## IP Address Extraction

The `log_action()` helper extracts the client IP from the request, handling reverse proxies:

```python
def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")
```

---

## Database Table

Table name: `iam_audit_log`

Indexed columns: `action`, `timestamp` — supports fast filtering by event type and date range.

---

## Implementation Status

- [x] `AuditLog` model created
- [ ] `log_action()` helper
- [ ] Auth events (login, logout, refresh)
- [ ] User management events (create, update, delete, reset password)
- [ ] Department events (create, update, delete)
- [ ] Audit log API endpoint (list/filter)
- [ ] Audit log UI page
