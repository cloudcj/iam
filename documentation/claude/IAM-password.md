# IAM Password Management

## Overview

There are three password-related operations in the IAM system:

| Operation | Who | Endpoint |
|---|---|---|
| Change own password | Authenticated user | `POST /api/v1/me/change-password/` |
| Reset another user's password | Admin | `POST /api/v1/identity/users/{user_id}/reset-password/` |
| Force password change on first login | System-enforced | Triggered automatically on user creation / admin reset |

---

## Force Password Change (First Login)

### How it works

When a user account is **created** or an admin **resets** a user's password, the system sets `must_change_password = True` on that user.

On the next login:
- The access token will contain the claim `"must_change_password": true`
- Any protected endpoint (except `change-password`) will return `403` until the password is changed

### JWT Claim

After login, decode the access token. The claim will be present:

```json
{
  "username": "john.doe",
  "must_change_password": true,
  ...
}
```

> The access token is stored as an HttpOnly cookie. To read the claim, either:
> - Decode the JWT on the frontend (base64 decode the payload portion), OR
> - Use the `/api/v1/me/` endpoint — if `must_change_password` is `true`, the request will be blocked and return a `403`

### Blocked Response (403)

Any request to a protected endpoint while `must_change_password = true`:

```json
{
  "detail": "You must change your password before accessing this resource.",
  "code": "must_change_password"
}
```

### How to clear the flag

Call `POST /api/v1/me/change-password/`. On success, the flag is cleared and fresh tokens are issued automatically — no need to re-login.

---

## Change Own Password

**Endpoint:** `POST /api/v1/me/change-password/`

**Auth:** Requires valid access token (HttpOnly cookie or `Authorization: Bearer`)

> This endpoint is accessible even when `must_change_password = true`.

### Request

```json
{
  "current_password": "old_password_here",
  "new_password": "new_password_here",
  "confirm_password": "new_password_here"
}
```

| Field | Required | Notes |
|---|---|---|
| `current_password` | ✅ | Must match the current stored password |
| `new_password` | ✅ | Minimum 8 characters |
| `confirm_password` | ✅ | Must match `new_password` |

### Success Response (200)

```json
{
  "detail": "Password changed successfully."
}
```

Fresh auth cookies (`access`, `refresh`) are set in the response — the user remains logged in with updated tokens.

### Error Responses

| Status | Body | Reason |
|---|---|---|
| `400` | `{"current_password": ["Incorrect password."]}` | Wrong current password |
| `400` | `{"confirm_password": ["Passwords do not match."]}` | `new_password` ≠ `confirm_password` |
| `400` | `{"new_password": ["...min 8 characters..."]}` | Password too short |
| `401` | `{"detail": "..."}` | Not authenticated |

---

## Admin: Reset Another User's Password

**Endpoint:** `POST /api/v1/identity/users/{user_id}/reset-password/`

**Required permission:** `iam.user.reset_password`

**Auth:** Requires valid access token

### Actor Restrictions

| Actor | Can reset |
|---|---|
| Superuser | Any user |
| Platform Admin | Any user except superusers and other platform admins |
| Dept Admin | Only users in their own department |

### Request

```json
{
  "new_password": "temporary_password123"
}
```

### Success Response (200)

```json
{
  "detail": "Password reset successfully."
}
```

> After this call, `must_change_password` is set to `true` on the target user. The next time they log in, they will be forced to change their password before accessing anything.

### Error Responses

| Status | Body | Reason |
|---|---|---|
| `404` | `{"detail": "User not found."}` | Invalid `user_id` |
| `403` | `{"detail": "You do not have permission to reset a superuser's password."}` | Actor is not superuser |
| `403` | `{"detail": "You do not have permission to reset another platform admin's password."}` | Platform admin trying to reset another platform admin |
| `403` | `{"detail": "You can only reset passwords for users in your department."}` | Dept admin, wrong dept |

---

## Frontend Integration Guide

### On Login

1. After a successful login (`POST /api/v1/auth/login/`), decode the access JWT cookie payload (base64 decode middle segment).
2. Check the `must_change_password` claim.
3. If `true` → redirect user to a "Change Password" page before allowing access to any other route.

```ts
function getMustChangePassword(): boolean {
  const token = getCookie("access"); // read HttpOnly is NOT possible — see note below
  // ...
}
```

> **Note:** Because the `access` cookie is `HttpOnly`, JavaScript cannot read it directly. Instead, attempt a request to `GET /api/v1/me/` after login:
> - If `200` → user is fine
> - If `403` with `"code": "must_change_password"` → redirect to change-password page

### On Change Password Page

- Call `POST /api/v1/me/change-password/`
- On `200` → proceed to the normal authenticated flow (tokens are already refreshed in the cookies)
- On `400` → show field-level errors

---

## Summary of `must_change_password` Triggers

| Trigger | Sets flag |
|---|---|
| New user created via IAM | ✅ `true` |
| Admin resets user password | ✅ `true` |
| User changes own password | ✅ cleared to `false` |
| Token refresh | No change — reflects current DB value |
