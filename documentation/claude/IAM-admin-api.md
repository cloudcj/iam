# IAM Admin — API Reference

**Base URL:** `http://<host>/api/v1`

All endpoints (except `/auth/csrf/` and `/auth/login/`) require a valid JWT passed via:
- **Browser:** HttpOnly cookie (set automatically on login) + `X-CSRFToken` header
- **M2M / Postman:** `Authorization: Bearer <access_token>` header

> **Browser clients must call `GET /api/v1/auth/csrf/` before any mutating request** to obtain the CSRF cookie.

---

## Table of Contents

1. [Authentication](#1-authentication)
2. [Current User (Me)](#2-current-user-me)
3. [Users](#3-users)
4. [Departments](#4-departments)
5. [Roles](#5-roles)
6. [Permissions](#6-permissions)
7. [Policies](#7-policies)
8. [Permission Summary](#8-permission-summary)

---

## 1. Authentication

### Get CSRF Token
```
GET /api/v1/auth/csrf/
```
Sets the `csrftoken` cookie. Call this before login or any mutating request from a browser.

**Response `200 OK`:**
```json
{ "detail": "CSRF cookie set." }
```

---

### Login
```
POST /api/v1/auth/login/
```
**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response `200 OK`:** Sets `access_token` and `refresh_token` HttpOnly cookies.
```json
{
  "user": {
    "id": "uuid",
    "username": "string",
    "email": "string",
    "is_superuser": false,
    "department": { "code": "string", "name": "string" },
    "systems": ["iam", "tropos"],
    "permissions": ["iam.user.read", "..."]
  }
}
```

| Code | Reason |
|---|---|
| `400` | Missing credentials |
| `401` | Invalid username or password |

---

### Logout
```
POST /api/v1/auth/logout/
```
Clears cookies and blacklists the refresh token.

**Response `200 OK`:**
```json
{ "detail": "Logged out successfully." }
```

---

### Refresh Token
```
POST /api/v1/auth/refresh/
```
Rotates the refresh token and issues a new access token. Called automatically by the frontend on 401.

**Response `200 OK`:** Sets new `access_token` cookie.

| Code | Reason |
|---|---|
| `401` | Refresh token expired or blacklisted |

---

## 2. Current User (Me)

### Get My Profile
```
GET /api/v1/me/
```
Returns the logged-in user's profile, permissions, and accessible systems. No special permission required — authenticated only.

**Response `200 OK`:**
```json
{
  "id": "uuid",
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "is_superuser": false,
  "department": {
    "code": "string",
    "name": "string"
  },
  "systems": ["iam", "tropos"],
  "permissions": ["iam.user.read", "iam.user.create", "..."]
}
```

---

### Update My Profile
```
PATCH /api/v1/me/profile/
```
Authenticated only. Users can update their own first name, last name, and email.

**Request Body:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string"
}
```

**Response `200 OK`:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string"
}
```

| Code | Reason |
|---|---|
| `400` | Email already in use or validation error |

---

### Change My Password
```
POST /api/v1/me/change-password/
```
Authenticated only. Requires the current password for verification.

**Request Body:**
```json
{
  "current_password": "string",
  "new_password": "string",       // min 8 characters
  "confirm_password": "string"
}
```

**Response `200 OK`:**
```json
{ "detail": "Password changed successfully." }
```

| Code | Reason |
|---|---|
| `400` | Incorrect current password, passwords don't match, or too short |

---

### Get Accessible Systems
```
GET /api/v1/me/systems/
```
Returns the list of systems the current user has access to.

**Response `200 OK`:**
```json
{
  "systems": [
    { "code": "iam", "label": "IAM" },
    { "code": "tropos", "label": "Tropos" }
  ]
}
```

---

## 3. Users

### List Users
```
GET /api/v1/identity/users/
```
**Permission required:** `iam.user.read`

**Visibility scope (enforced server-side):**

| Actor | Sees |
|---|---|
| Superuser | All non-superuser users |
| Platform Admin / Viewer | All users except other platform-level users |
| Dept Admin / Viewer | Only users in their own department |

**Response `200 OK`:**
```json
[
  {
    "id": "uuid",
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "is_active": true,
    "department": {
      "id": "uuid",
      "code": "string",
      "name": "string"
    },
    "roles": ["role.code", "..."]
  }
]
```

---

### Get User Detail
```
GET /api/v1/identity/users/<user_id>/
```
**Permission required:** `iam.user.read`

**Response `200 OK`:**
```json
{
  "id": "uuid",
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "is_active": true,
  "department": "uuid",
  "roles": ["uuid", "..."],
  "permission_codes": ["iam.user.read", "..."],
  "extra_permission_ids": ["uuid", "..."]
}
```

> `permission_codes` — all resolved permission codes (from roles + direct assignments)
> `extra_permission_ids` — IDs of permissions assigned directly to the user (not via role)

---

### Create User
```
POST /api/v1/identity/users/create/
```
**Permission required:** `iam.user.create`

**Request Body:**
```json
{
  "username": "string",           // required, unique
  "password": "string",           // required, min 8 characters
  "first_name": "string",         // required
  "last_name": "string",          // required
  "email": "string",              // required, unique
  "department": "uuid",           // required (ignored for dept admin — auto-set to their dept)
  "roles": ["uuid", "..."],       // required, min 1
  "permissions": ["uuid", "..."]  // optional, direct permission assignments
}
```

**Actor restrictions:**
- **Dept Admin:** `department` is auto-set; cannot assign platform-level roles
- **Platform Admin:** cannot assign the `platform.admin` role

**Response `201 Created`:**
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "department": {
    "id": "uuid",
    "code": "string",
    "name": "string"
  }
}
```

| Code | Reason |
|---|---|
| `400` | Duplicate username/email, invalid roles, missing fields |
| `403` | Insufficient permission or role scope violation |

---

### Update User
```
PATCH /api/v1/identity/users/<user_id>/update/
```
**Permission required:** `iam.user.update`

**Request Body:**
```json
{
  "username": "string",              // optional, superuser only
  "first_name": "string",           // required
  "last_name": "string",            // required
  "email": "string",                // required
  "department": "uuid",             // required
  "roles": ["uuid", "..."],         // required, min 1
  "permission_ids": ["uuid", "..."] // optional
}
```

> `username` is only applied when the actor is a **superuser**. Changing username invalidates the user's active tokens within 15 minutes (JWT expiry).

**Permission replacement behavior:**

| Actor | Behavior |
|---|---|
| Superuser | Full override — replaces all permissions with `permission_ids` |
| Platform Admin | Replaces role-derived and direct permissions with new values |
| Dept Admin | Only replaces role-derived permissions; direct permissions untouched |

**Response `200 OK`:**
```json
{
  "id": "uuid",
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "is_active": true
}
```

| Code | Reason |
|---|---|
| `400` | Duplicate email, invalid roles |
| `403` | Role scope violation |
| `404` | User not found |

---

### Delete User (Soft Delete)
```
DELETE /api/v1/identity/users/<user_id>/delete/
```
**Permission required:** `iam.user.delete`

Sets `is_active = false`. The user record is **not** permanently removed.

**Rules:**
- Cannot delete yourself
- Dept Admins: can only delete users in their own department; cannot delete platform-level users

**Response `200 OK`:**
```json
{ "detail": "User deactivated." }
```

| Code | Reason |
|---|---|
| `400` | User already deactivated |
| `403` | Self-delete or insufficient scope |
| `404` | User not found |

---

### Reset User Password (Admin)
```
POST /api/v1/identity/users/<user_id>/reset-password/
```
**Permission required:** `iam.user.reset_password`

Admin resets another user's password. Current password is **not** required.

**Request Body:**
```json
{
  "new_password": "string",      // min 8 characters
  "confirm_password": "string"
}
```

**Actor restrictions:**

| Actor | Can Reset |
|---|---|
| Superuser | Any user |
| Platform Admin | Any non-superuser, non-platform-admin user |
| Dept Admin | Users in their own department only |

**Response `200 OK`:**
```json
{ "detail": "Password reset successfully." }
```

| Code | Reason |
|---|---|
| `400` | Passwords don't match or too short |
| `403` | Target is superuser, platform admin, or outside actor's department |
| `404` | User not found |

---

## 4. Departments

### List Departments
```
GET /api/v1/department/
```
**Permission required:** `iam.department.read`

**Response `200 OK`:**
```json
[
  {
    "id": "uuid",
    "code": "string",
    "name": "string",
    "allowed_systems": ["tropos", "ghidora"]
  }
]
```

---

### Create Department
```
POST /api/v1/department/create/
```
**Permission required:** `iam.department.create`

**Request Body:**
```json
{
  "name": "string",                      // required; auto-generates code (e.g. "Cloud Ops" → "CLOUD_OPS")
  "allowed_systems": ["tropos", "..."]  // required, min 1
}
```

**Response `201 Created`:**
```json
{
  "id": "uuid",
  "code": "string",
  "name": "string",
  "allowed_systems": ["tropos"]
}
```

| Code | Reason |
|---|---|
| `400` | Name taken, no systems provided |

---

### Update Department
```
PATCH /api/v1/department/<department_id>/update/
```
**Permission required:** `iam.department.update`

**Request Body:**
```json
{
  "name": "string",
  "allowed_systems": ["tropos", "..."]
}
```

**Rules:**
- The `GLOBAL` department cannot be edited

**Response `200 OK`:**
```json
{
  "id": "uuid",
  "code": "string",
  "name": "string",
  "allowed_systems": ["tropos"]
}
```

| Code | Reason |
|---|---|
| `400` | Name taken, no systems provided |
| `403` | Attempt to edit the GLOBAL department |
| `404` | Department not found |

---

### Delete Department
```
DELETE /api/v1/department/<department_id>/delete/
```
**Permission required:** `iam.department.delete`

**Rules:**
- The `GLOBAL` department cannot be deleted
- Departments with assigned users cannot be deleted

**Response `200 OK`:**
```json
{ "detail": "Department deleted." }
```

| Code | Reason |
|---|---|
| `400` | Department still has users assigned |
| `403` | Attempt to delete the GLOBAL department |
| `404` | Department not found |

---

## 5. Roles

### List Roles
```
GET /api/v1/access/roles/
```
No special permission required — authenticated only.

Returns all roles with their associated policies and permission codes. Used by the frontend to build role dropdowns and compute permission presets.

**Response `200 OK`:**
```json
[
  {
    "id": "uuid",
    "code": "tropos.admin",
    "name": "Tropos Admin",
    "system": "tropos",
    "policies": [
      {
        "id": "uuid",
        "code": "tropos.full",
        "name": "Tropos – Full Access",
        "system": "tropos",
        "resource": "*",
        "description": "",
        "permission_codes": ["tropos.region.read", "tropos.region.create", "..."]
      }
    ]
  }
]
```

---

## 6. Permissions

### List Permissions
```
GET /api/v1/access/permissions/
```
No special permission required — authenticated only.

Returns all permission records. Used by the frontend to render permission checkboxes.

**Response `200 OK`:**
```json
[
  {
    "id": "uuid",
    "code": "iam.user.read",
    "system": "iam",
    "resource": "user",
    "action": "read",
    "description": ""
  }
]
```

---

## 7. Policies

### List Policies
```
GET /api/v1/access/policies/
```
No special permission required — authenticated only.

Returns all policies with their permission codes. Used as a fallback by the frontend when roles don't include inline `permission_codes`.

**Response `200 OK`:**
```json
[
  {
    "id": "uuid",
    "code": "iam.user.full",
    "name": "IAM Users – Manage",
    "system": "iam",
    "resource": "user",
    "description": "",
    "permission_codes": ["iam.user.read", "iam.user.create", "..."]
  }
]
```

---

## 8. Permission Summary

| Endpoint | Method | Permission Code |
|---|---|---|
| List Users | `GET` | `iam.user.read` |
| Get User Detail | `GET` | `iam.user.read` |
| Create User | `POST` | `iam.user.create` |
| Update User | `PATCH` | `iam.user.update` |
| Delete User | `DELETE` | `iam.user.delete` |
| Reset User Password | `POST` | `iam.user.reset_password` |
| List Departments | `GET` | `iam.department.read` |
| Create Department | `POST` | `iam.department.create` |
| Update Department | `PATCH` | `iam.department.update` |
| Delete Department | `DELETE` | `iam.department.delete` |
| List Roles | `GET` | *(authenticated only)* |
| List Permissions | `GET` | *(authenticated only)* |
| List Policies | `GET` | *(authenticated only)* |
| Get My Profile | `GET` | *(authenticated only)* |
| Update My Profile | `PATCH` | *(authenticated only)* |
| Change My Password | `POST` | *(authenticated only)* |
| Get My Systems | `GET` | *(authenticated only)* |
| Login | `POST` | *(public)* |
| Logout | `POST` | *(authenticated only)* |
| Refresh Token | `POST` | *(authenticated only)* |
| Get CSRF Token | `GET` | *(public)* |
