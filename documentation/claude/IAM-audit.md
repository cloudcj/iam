# IAM Audit Log

## Overview

Every significant action in the IAM system is recorded — who did it, what they did, what was affected, and whether it succeeded or failed. Logs are stored in `iam_audit_log` and exposed via a filterable, paginated API.

---

## API Reference

### List Audit Logs

```
GET /api/v1/audit/logs/
```

**Auth:** JWT cookie or `Authorization: Bearer <token>`  
**Permission:** `iam.audit.read` or superuser

#### Query Parameters

| Param | Type | Description |
|---|---|---|
| `action` | string | Exact action code — e.g. `auth.login`, `user.create` |
| `action_category` | `auth` \| `activity` | `auth` → all `auth.*` events; `activity` → all non-auth events |
| `status` | `success` \| `failure` | Filter by outcome |
| `target_type` | string | `user` or `department` |
| `date_from` | `YYYY-MM-DD` | Start date (inclusive) |
| `date_to` | `YYYY-MM-DD` | End date (inclusive) |
| `limit` | integer | Page size (max `200`, default `50`) |
| `offset` | integer | Pagination offset |

> `action` and `action_category` can be combined — e.g. `action_category=auth&status=failure` returns all failed auth events.

#### Response

```json
{
  "count": 120,
  "results": [
    {
      "id": "uuid",
      "actor": "jdoe",
      "actor_name": "John Doe",
      "department": "Cloud Platform",
      "action": "auth.login",
      "target_id": "uuid",
      "target_type": "user",
      "status": "success",
      "detail": {
        "username": "jdoe",
        "browser": "Chrome 120",
        "os": "Windows 11",
        "device": "Desktop"
      },
      "ip_address": "192.168.1.1",
      "timestamp": "2026-04-01T08:00:00.000000"
    }
  ]
}
```

#### Response Fields

| Field | Description |
|---|---|
| `id` | UUID of the log entry |
| `actor` | Username of who performed the action (`null` for anonymous) |
| `actor_name` | Full name of the actor (`null` for anonymous) |
| `department` | Actor's department name at the time of the action |
| `action` | Action code — see [Action Reference](#action-reference) |
| `target_id` | UUID of the affected object (user, department) |
| `target_type` | Type of affected object: `"user"`, `"department"` |
| `status` | `"success"` or `"failure"` |
| `detail` | JSON object with extra context — varies by action |
| `ip_address` | Client IP address |
| `timestamp` | ISO 8601 datetime |

---

## Action Reference

### Authentication (`action_category=auth`)

| Code | Label | Triggered When |
|---|---|---|
| `auth.login` | Login | Successful login |
| `auth.login_failed` | Login Failed | Wrong password or unknown username |
| `auth.logout` | Logout | User logged out |
| `auth.token_refresh` | Token Refresh | JWT access token refreshed |
| `auth.account_locked` | Account Locked | Login blocked — 5 consecutive failures reached |

### Activity (`action_category=activity`)

| Code | Label | Triggered When |
|---|---|---|
| `user.create` | User Created | New user created |
| `user.update` | User Updated | User record updated |
| `user.delete` | User Deleted | User deactivated |
| `user.reset_password` | Password Reset | Admin reset a user's password |
| `user.change_password` | Password Changed | User changed their own password |
| `department.create` | Department Created | New department created |
| `department.update` | Department Updated | Department record updated |
| `department.delete` | Department Deleted | Department deleted |

---

## `detail` Field Reference

Contents vary by action. Auth events automatically include user agent info.

### `auth.login`
```json
{ "username": "jdoe", "browser": "Chrome 120", "os": "Windows 11", "device": "Desktop" }
```

### `auth.login_failed`
```json
{ "username": "jdoe", "reason": "Invalid credentials", "browser": "Chrome 120", "os": "Windows 11", "device": "Desktop" }
```

### `auth.account_locked`
```json
{ "username": "jdoe", "browser": "Chrome 120", "os": "Windows 11", "device": "Desktop" }
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

### `department.create` / `department.update` / `department.delete`
```json
{ "name": "Engineering", "code": "ENGINEERING" }
```

---

## Account Lockout

Failed logins are tracked in Redis per username. After 5 consecutive failures, the account is temporarily locked.

| Setting | Value |
|---|---|
| Max attempts | `5` |
| Lockout duration | `15 minutes` |
| Redis key | `iam:lockout:<username>` |

**Behavior:**
- Each failed login increments the Redis counter (TTL resets to 15 min on each failure)
- On the 5th failure, all subsequent attempts return `403` and are logged as `auth.account_locked`
- A successful login clears the counter immediately

---

## Backend Reference

### Model (`apps/audit/models.py`)

```python
class AuditLog(models.Model):
    id          # UUID primary key
    actor       # FK → User (nullable — anonymous for failed logins)
    action      # CharField — must use AuditLog.Action choices
    target_id   # UUID of affected object (nullable)
    target_type # "user" | "department" (blank for auth events)
    status      # "success" | "failure"
    detail      # JSONField — extra context
    ip_address  # Client IP
    timestamp   # Auto-set, indexed
```

### Logging (`apps/audit/services/services.py`)

Never write to `AuditLog` directly — always use `log_action()`:

```python
from apps.audit.services.services import log_action
from apps.audit.models import AuditLog

log_action(
    actor=request.user,                    # User instance or None
    action=AuditLog.Action.USER_CREATE,
    target_id=user.id,                     # optional
    target_type="user",                    # optional
    status=AuditLog.Status.SUCCESS,        # default: SUCCESS
    detail={"username": user.username},
    request=request,                       # extracts IP + user agent automatically
)
```

When `request` is provided, `browser`, `os`, and `device` are automatically added to `detail`.

### Adding a New Action Type

1. Add to `AuditLog.Action` in `apps/audit/models.py`
2. Call `log_action()` with the new action in the relevant service/view
3. Run `python manage.py makemigrations audit && python manage.py migrate`
4. Add the label to `AUTH_ACTION_LABELS` or `ACTIVITY_ACTION_LABELS` in `AuditLogPage.tsx`

---

## Frontend Reference

### RTK Query (`iamApi.ts`)

```typescript
const { data, isLoading } = useGetAuditLogsQuery({
  action_category: 'auth',
  status: 'failure',
  limit: 20,
  offset: 0,
})
```

### Types (`types/index.ts`)

```typescript
interface AuditLogParams {
  action?: string
  action_category?: string   // 'auth' | 'activity'
  status?: string
  target_type?: string
  date_from?: string
  date_to?: string
  limit?: number
  offset?: number
}

interface AuditLog {
  id: string
  actor: string | null
  actor_name: string | null
  department: string | null
  action: string
  target_id: string | null
  target_type: string
  status: 'success' | 'failure'
  detail: Record<string, any>
  ip_address: string | null
  timestamp: string
}

interface AuditLogResponse {
  count: number
  results: AuditLog[]
}
```

### UI (`AuditLogPage.tsx`)

Two tabs, each with independent filters and pagination:

| Tab | `action_category` | Action dropdown options |
|---|---|---|
| Login Activity | `auth` | Login, Login Failed, Logout, Token Refresh, Account Locked |
| Activity Log | `activity` | All user and department management actions |

Switching tabs resets all filters and returns to page 1.
