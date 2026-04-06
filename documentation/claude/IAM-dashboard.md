# Dashboard API

## Overview

The Dashboard API provides a single aggregated endpoint for admin dashboards. Instead of making multiple API calls for stats, audit logs, and department data, the frontend calls one endpoint that efficiently queries the database and returns all dashboard data.

## Endpoint

```
GET /api/v1/dashboard/summary/
```

## Authentication & Authorization

- **Requires:** `IsAuthenticated` + `HasPermission`
- **Required Permission:** `iam.audit.read`

Only users with audit read permission can access the dashboard (typically admins).

## Response Schema

```json
{
  "stats": {
    "total_users": number,
    "active_users": number,
    "inactive_users": number,
    "total_departments": number
  },
  "users_by_department": [
    {
      "name": string,
      "user_count": number
    }
  ],
  "failed_logins_7d": number,
  "login_success_7d": number,
  "recent_activity": [
    {
      "id": string,
      "actor": string | null,
      "actor_name": string | null,
      "action": string,
      "status": "success" | "failure",
      "ip_address": string | null,
      "timestamp": string (ISO 8601)
    }
  ],
  "top_actors": [
    {
      "username": string,
      "name": string,
      "event_count": number
    }
  ],
  "recent_admin_actions": [
    {
      "id": string,
      "actor": string | null,
      "actor_name": string | null,
      "action": string,
      "target_type": string,
      "status": "success" | "failure",
      "timestamp": string (ISO 8601)
    }
  ]
}
```

## Response Fields

### `stats`
System-wide statistics.

| Field | Type | Description |
|-------|------|-------------|
| `total_users` | number | Total user count |
| `active_users` | number | Count of active (`is_active=True`) users |
| `inactive_users` | number | Count of inactive users (derived from total - active) |
| `total_departments` | number | Total department count |

### `users_by_department`
User distribution across departments (ordered by count descending).

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Department name |
| `user_count` | number | Count of users in this department |

### `failed_logins_7d` & `login_success_7d`
Login statistics for the last 7 days.

- `failed_logins_7d`: Count of `auth.login_failed` events in the last 7 days
- `login_success_7d`: Count of `auth.login` events with `status=success` in the last 7 days

### `recent_activity`
Last 10 audit log entries (all action types).

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Audit log UUID |
| `actor` | string \| null | Username of the actor (null for anonymous/failed logins) |
| `actor_name` | string \| null | Full name of the actor |
| `action` | string | Action code (e.g., `auth.login`, `user.create`) |
| `status` | "success" \| "failure" | Event outcome |
| `ip_address` | string \| null | IP address of the request |
| `timestamp` | string | ISO 8601 timestamp |

### `top_actors`
Top 5 most active users in the last 7 days.

| Field | Type | Description |
|-------|------|-------------|
| `username` | string | Actor's username |
| `name` | string | Actor's full name |
| `event_count` | number | Number of events triggered by this user (last 7 days) |

### `recent_admin_actions`
Last 10 administrative actions (user/department create/update/delete/reset-password).

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Audit log UUID |
| `actor` | string \| null | Username of the admin |
| `actor_name` | string \| null | Full name of the admin |
| `action` | string | Admin action code |
| `target_type` | string | Type of target (`user`, `department`) |
| `status` | "success" \| "failure" | Whether the action succeeded |
| `timestamp` | string | ISO 8601 timestamp |

## Admin Action Types

The `recent_admin_actions` array includes these action types:

- `user.create` — User created
- `user.update` — User updated
- `user.delete` — User deleted
- `user.reset_password` — Password reset
- `department.create` — Department created
- `department.update` — Department updated
- `department.delete` — Department deleted

## Example Request

```bash
curl -X GET http://localhost:8000/api/v1/dashboard/summary/ \
  -H "Authorization: Bearer <access_token>" \
  -H "X-CSRFToken: <csrf_token>" \
  -H "Content-Type: application/json"
```

## Example Response

```json
{
  "stats": {
    "total_users": 42,
    "active_users": 38,
    "inactive_users": 4,
    "total_departments": 5
  },
  "users_by_department": [
    { "name": "Engineering", "user_count": 18 },
    { "name": "Sales", "user_count": 12 },
    { "name": "HR", "user_count": 8 },
    { "name": "Finance", "user_count": 4 }
  ],
  "failed_logins_7d": 3,
  "login_success_7d": 87,
  "recent_activity": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "actor": "john.doe",
      "actor_name": "John Doe",
      "action": "user.create",
      "status": "success",
      "ip_address": "192.168.1.1",
      "timestamp": "2026-04-06T14:30:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "actor": null,
      "actor_name": null,
      "action": "auth.login_failed",
      "status": "failure",
      "ip_address": "203.0.113.45",
      "timestamp": "2026-04-06T14:28:15Z"
    }
  ],
  "top_actors": [
    { "username": "john.doe", "name": "John Doe", "event_count": 24 },
    { "username": "jane.smith", "name": "Jane Smith", "event_count": 18 }
  ],
  "recent_admin_actions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "actor": "john.doe",
      "actor_name": "John Doe",
      "action": "user.create",
      "target_type": "user",
      "status": "success",
      "timestamp": "2026-04-06T14:30:00Z"
    }
  ]
}
```

## Performance Notes

- **Single Database Call:** All data is aggregated in one view using Django ORM annotations and efficient queries.
- **Caching:** RTK Query on the frontend caches the response. Refetch as needed via `invalidateTags`.
- **7-Day Window:** Login stats and top actors use a 7-day sliding window (`now() - timedelta(days=7)`).
- **Limits:** Last 10 recent activity entries, last 5 top actors, last 10 admin actions.

## Frontend Usage

```typescript
// In React component
import { useGetDashboardSummaryQuery } from '../services/iamApi'

function Dashboard() {
  const { data: dashboard, isLoading } = useGetDashboardSummaryQuery()
  
  if (!dashboard) return <div>Loading...</div>
  
  return (
    <div>
      <p>Total Users: {dashboard.stats.total_users}</p>
      <p>Failed Logins (7d): {dashboard.failed_logins_7d}</p>
    </div>
  )
}
```

## Implementation Files

| File | Purpose |
|------|---------|
| `apps/dashboard/views.py` | `DashboardSummaryView` — main view logic |
| `apps/dashboard/urls.py` | Route: `/dashboard/summary/` |
| `apps/dashboard/apps.py` | Django app config |
| `z-frontend/.../services/iamApi.ts` | RTK Query hook: `useGetDashboardSummaryQuery` |
| `z-frontend/.../pages/DashboardPage.tsx` | React component using the API |
| `z-frontend/.../types/index.ts` | TypeScript types: `DashboardSummary` |

## Error Handling

- **401 Unauthorized:** User is not logged in or token expired
- **403 Forbidden:** User lacks `iam.audit.read` permission
- **500 Server Error:** Database connectivity or unexpected error

The frontend's `baseQueryWithReauth` middleware handles 401s by attempting a token refresh before re-raising the error.
