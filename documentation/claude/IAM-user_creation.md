# IAM User Creation Rules

## Overview

User creation rules are enforced based on the actor's (creator's) role.
Permissions are the source of truth — roles and policies are UI presets only.

At creation time:
```
Role selected → Role → Policy → Permission → UserPermission saved (source="role")
```

No direct permission selection at creation. That belongs to post-creation update.

---

## Superuser

### Who can create
- Any user in any department

### Department assignment
- Any department — required field
- Use GLOBAL for platform-level users

### Role assignment
- Any role including `platform.admin`, `platform.viewer`, `dept.admin`, `dept.viewer`
- No scope restrictions

### Permission assignment
- Automatically expanded from selected roles
- Cannot uncheck permissions at creation
- Post-creation: can add/remove any permission with no scope limit

### Additional rules
- Only superuser can create a `platform.admin` account
- Cannot be created via IAM UI — database/seeder only (`is_superuser=True`)
- Bypasses all permission checks at runtime

---

## Platform Admin (`platform.admin`)

### Who can create
- Any user in any department

### Department assignment
- Any department — required field

### Role assignment
- Any role **except** `platform.admin`
- Roles must belong to the department's `allowed_systems`
- Can assign `dept.admin`, `dept.viewer`, and system-specific roles within dept scope

### Permission assignment
- Automatically expanded from selected roles
- Cannot uncheck permissions at creation
- Post-creation: can add/remove any permission within department scope (including role-based)

### Additional rules
- Cannot create another `platform.admin` — superuser only
- Can see all users across all departments

---

## Department Admin (`dept.admin`)

### Who can create
- Users within their own department only

### Department assignment
- Automatically set to actor's own department
- Input is ignored — cannot assign a different department

### Role assignment
- Cannot assign hidden roles: `platform.admin`, `platform.viewer`, `dept.admin`, `dept.viewer`
- Can only assign roles where `role.code.split(".")[0]` is in `department.allowed_systems`

### Permission assignment
- Automatically expanded from selected roles
- Cannot uncheck permissions at creation
- Post-creation: role change only — no direct permission control

### Additional rules
- Cannot see users outside their own department
- Cannot see users with hidden roles even in own department
- Cannot move users between departments

---

## Role Assignment Authority Summary

| Role to assign | Superuser | Platform Admin | Dept Admin |
|---|---|---|---|
| `platform.admin` | ✅ | ❌ | ❌ |
| `platform.viewer` | ✅ | ❌ | ❌ |
| `dept.admin` | ✅ | ✅ | ❌ |
| `dept.viewer` | ✅ | ✅ | ❌ |
| `{system}.admin/viewer` | ✅ | ✅ dept scoped | ✅ dept scoped |

---

## Department Assignment Summary

| Actor | Can assign any dept | Auto-sets dept | Dept required |
|---|---|---|---|
| Superuser | ✅ | ❌ | ✅ |
| Platform Admin | ✅ | ❌ | ✅ |
| Dept Admin | ❌ | ✅ (own dept) | ❌ (ignored) |

---

## Post-Creation Permission Control

| Actor | Role update | Add/remove permissions | Move dept |
|---|---|---|---|
| Superuser | Any | Any, no scope limit | ✅ |
| Platform Admin | Dept scoped | Dept scoped (including role-based) | ✅ |
| Dept Admin | Dept scoped | ❌ not allowed | ❌ |

### How post-creation permission update works (UI)
1. View current permissions grouped by system/resource
2. Check/uncheck individual permissions
3. Use policy presets as shortcuts to bulk-check a permission group
4. API receives only permission UUIDs — policy is never saved

---

## User Deactivation & Deletion

| Actor | Can deactivate/delete |
|---|---|
| Superuser | Any user |
| Platform Admin | Any user except superusers |
| Dept Admin | Only non-hidden-role users in their department |

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

---

## User Visibility Rules

| Actor | Can see |
|---|---|
| Superuser | All users, all departments |
| Platform Admin | All users, all departments |
| Platform Viewer | All users, all departments |
| Dept Admin | Own department only, excludes hidden-role users |
| Dept Viewer | Own department only, excludes hidden-role users |

Superusers (`is_superuser=True`) are always excluded from listing regardless of actor.
