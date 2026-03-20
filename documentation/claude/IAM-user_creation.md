# IAM User Creation Rules

## Overview

User creation rules are enforced based on the actor's (creator's) role. Each role has a defined scope of what they can set when creating a user.

---

## Superuser

### Who can create
- Anyone (all users, all departments)

### Department assignment
- Can assign any department including global (no department)

### Role & Policy assignment
- Can assign any role including `platform.admin`, `platform.viewer`, `dept.admin`
- Can assign any policy regardless of system or department scope

### Additional rules
- Only superuser can create a `platform.admin` account
- Only superuser can assign the `platform.admin` and `platform.viewer` roles
- Can change a user's department at any time after creation
- Can deactivate or delete any user
- Cannot be created via IAM UI — must be set directly in the database (`is_superuser=True`)

---

## Platform Admin (`platform.admin`)

### Who can create
- Any user in any department

### Department assignment
- Can assign any department including global (no department)

### Role & Policy assignment
- Can assign any role **except** `platform.admin`
- Can assign `dept.admin`, `dept.viewer`, and all system-specific roles
- Can assign any policy regardless of system or department scope

### Additional rules
- Cannot create another `platform.admin` — superuser only
- Can change a user's department at any time after creation
- Can deactivate or delete any user except superuser accounts
- Can see all users across all departments

---

## Department Admin (`dept.admin`)

### Who can create
- Users within their own department only

### Department assignment
- Department is automatically set to the actor's department
- Cannot assign a different department — locked to own department
- Cannot change a user's department after creation

### Role & Policy assignment
- Can only assign roles and policies scoped to their department's systems
- Cannot assign hidden roles: `platform.admin`, `platform.viewer`, `dept.admin`, `dept.viewer`
- Cannot assign policies outside the department's allowed systems

### Additional rules
- Cannot see users outside their own department
- Cannot deactivate or delete users with hidden roles
- Cannot modify their own account
- Cannot modify accounts of users with higher-tier roles

---

## Role & Policy Assignment Summary

| Actor | Can assign `platform.admin` | Can assign `dept.admin` | Can assign system roles | Can assign any policy |
|---|---|---|---|---|
| Superuser | Yes | Yes | Yes | Yes |
| Platform Admin | No | Yes | Yes | Yes |
| Dept Admin | No | No | Own dept only | Own dept only |

---

## Department Assignment Summary

| Actor | Can assign any dept | Can assign global | Auto-sets dept |
|---|---|---|---|
| Superuser | Yes | Yes | No |
| Platform Admin | Yes | Yes | No |
| Dept Admin | No | No | Yes (own dept) |

---

## Multiple Roles & Policies

- A user can have **one role** as their primary role (assigned via `UserRole`)
- A user can have **additional direct policy assignments** via `UserPolicy` for temporary or exception access
- Final permissions = policies from role + direct policy assignments
- Direct policy assignments are useful for temporary access without changing the user's primary role

---

## User Deactivation & Deletion

| Actor | Can deactivate/delete |
|---|---|
| Superuser | Any user |
| Platform Admin | Any user except superusers |
| Dept Admin | Only users in their department (non-hidden roles only) |

---

## Password & Account Setup

- Initial password is set at creation
- Password reset can be performed by:
  - Superuser → any user
  - Platform Admin → any user except superusers
  - Dept Admin → only users in their department
  - User themselves → own account only

---

## Superuser vs Platform Admin — Key Differences

| | Superuser | Platform Admin |
|---|---|---|
| Permission checks | Bypassed entirely | Goes through normal checks |
| Django Admin access | Yes | No |
| Can create `platform.admin` | Yes | No |
| JWT permissions | Empty `[]` (bypass flag) | All permission codes listed |
| Assigned via IAM UI | No — database only | Yes |
| New system added | Auto-access (bypasses all checks) | Must update role manually |
| Can be revoked | No (Django `is_superuser` flag) | Yes (remove role) |
| Auditable | No | Yes |
| Purpose | Break-glass, emergency access | Day-to-day platform management |
| Who gets it | 1–2 accounts max | Developers, platform managers |

### Important note on new systems
When a new system is added to the platform:
- **Superuser** automatically has access — bypasses all checks
- **Platform Admin** loses access to the new system until their role's policies are updated to include it

This is why superuser is reserved for emergencies and platform admin is used for day-to-day operations — platform admin access is explicit and auditable.

---

## User Visibility Rules

| Actor | Can see |
|---|---|
| Superuser | All users across all departments |
| Platform Admin | All users across all departments |
| Dept Admin | Only users in their own department |
