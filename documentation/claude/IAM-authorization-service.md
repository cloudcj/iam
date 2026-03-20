# IAM Authorization Service

## Overview

`AuthorizationService` is the core permission engine of the IAM system.
It answers one question: **"What can this user do?"**

Located at: `apps/authz/services/authorization_service.py`

---

## What It Does

| Method | Purpose | Used By |
|--------|---------|---------|
| `_load_permissions(user)` | Fetches all permission codes for a user (with caching) | Internal only |
| `has_permission(user, code)` | Returns True/False for a single permission check | `HasPermission`, `AuthorizeView` |
| `get_user_permission_codes(user)` | Returns full set of permission codes | JWT embedding, `/me/` |
| `get_user_systems(user)` | Returns which systems the user can access | JWT embedding, `/me/` |
| `group_permissions_by_system(codes)` | Groups permissions for frontend nav | `/me/` |
| `invalidate_cache(user_id)` | Clears Redis cache when permissions change | Admin permission updates |

---

## Permission Chain (DB Query)

When loading permissions from DB, it traverses this chain:

```
User
 └── UserPolicy
      └── Policy
           └── PolicyPermission
                └── Permission (code)
```

This means permissions are assigned to users via policies — never directly.

---

## Three-Layer Caching

Every permission lookup goes through 3 layers before hitting the DB:

```
Request comes in
    │
    ▼
1. user._cached_permission_codes    ← in-memory, lives on user object
   │ hit → return immediately           same request lifecycle only
   │ miss ↓
    ▼
2. Redis TTL cache (30s)            ← survives across requests
   │ hit → store on user object, return
   │ miss ↓
    ▼
3. DB query                         ← only on cold start or after invalidation
    │
    ▼
   Store in Redis (30s) + user object → return
```

### Why Three Layers?

| Layer | Scope | Cost | Purpose |
|-------|-------|------|---------|
| User object attribute | Single request | Zero | Multiple checks in one request hit DB only once |
| Redis (30s TTL) | Across requests | Near-zero | Login/refresh don't hammer DB |
| DB | Always fresh | Expensive | Source of truth |

---

## Why Redis Cache Matters at Login

After migrating to permissions-in-JWT, every login and token refresh
triggers `get_user_permission_codes()` to embed permissions in the token.

**Without Redis cache:**
```
User logs in          → DB query
User refreshes token  → DB query again
1000 users logging in → 1000 simultaneous DB queries
```

**With Redis cache (30s TTL):**
```
User logs in          → DB query → result cached in Redis
User refreshes token  → Redis hit → no DB query
1000 users logging in → first login per user hits DB
                         subsequent refreshes served from Redis
```

---

## Cache Invalidation

When an admin changes a user's permissions, the Redis cache must be cleared
so the next login/refresh picks up fresh data instead of stale cached data.

```python
# Call this after updating a user's policies/roles
AuthorizationService.invalidate_cache(user.id)
```

Without this, the user would keep old permissions for up to 30 seconds.

---

## Superuser Behavior

If `user.is_superuser = True`:
- Gets ALL permission codes from the Permission table
- Bypasses all permission checks in `HasPermission`
- JWT carries empty `permissions[]` (no need to embed — bypass happens locally)

```python
if user.is_superuser:
    permissions = set(Permission.objects.values_list("code", flat=True))
```

---

## group_permissions_by_system

Converts flat permission codes into a nested structure for frontend nav:

**Input:**
```python
{
    "tropos.az.read",
    "tropos.az.create",
    "tropos.room.read",
    "iam.user.read"
}
```

**Output:**
```json
{
    "tropos": {
        "az":   ["create", "read"],
        "room": ["read"]
    },
    "iam": {
        "user": ["read"]
    }
}
```

**Frontend uses this to:**
- Show/hide systems in top nav dropdown → user has any `tropos.*`
- Show/hide sidebar sections → user has any `tropos.az.*`
- Show/hide action buttons → user has `tropos.az.create`

---

## Permission Code Format

All permission codes follow the pattern: `system.resource.action`

```
tropos.az.read
├── system   = tropos
├── resource = az
└── action   = read
```

This format enables the 3-level frontend filtering:
```
Level 1 → system    → top nav dropdown visibility
Level 2 → resource  → sidebar menu item visibility
Level 3 → action    → button/feature visibility
```

---

## JWT Permission Embedding Flow

```
Login / Token Refresh
    │
    ▼
issue_user_tokens(user)
    │
    ├── get_user_permission_codes(user)
    │       └── _load_permissions() → 3-layer cache → returns set of codes
    │
    ├── get_user_systems(user)
    │       └── extracts system codes from permission codes
    │
    └── embeds into JWT:
            access["permissions"] = ["tropos.az.read", "iam.user.read", ...]
            access["systems"]     = ["tropos", "iam"]
```

Services then read permissions directly from the JWT token —
no IAM call needed per request.

---

## Related Files

| File | Role |
|------|------|
| `apps/authz/services/authorization_service.py` | This service |
| `apps/authz/permissions.py` | `HasPermission` DRF class — reads JWT permissions |
| `apps/authz/views/authorize.py` | `/authorize/` endpoint — real-time single permission check |
| `apps/authz/views/batch_authorize.py` | `/authorize/batch/` — real-time batch permission check |
| `apps/authn/tokens/service.py` | `issue_user_tokens` — embeds permissions in JWT |
| `apps/identity/views/me/me.py` | `/me/` — returns grouped permissions for frontend nav |
