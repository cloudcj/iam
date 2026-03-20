# IAM Roles & Hierarchy

## Overview

The IAM system uses a tiered role hierarchy. Each tier has a defined scope, set of rules, and who can assign it.

---

## Role Tiers

```
Tier 0 — Superuser          (Django built-in, bypasses everything)
Tier 1 — platform.admin     (all systems, all departments)
Tier 1 — platform.viewer    (read-only, all systems, all departments)
Tier 2 — dept.admin         (IAM user management, own department only)
Tier 2 — dept.viewer        (read-only, own department only)
Tier 3 — {system}.admin     (full access, specific system)
Tier 3 — {system}.viewer    (read-only, specific system)
```

---

## Tier 0 — Superuser

| Property | Value |
|---|---|
| Django flag | `is_superuser = True` |
| Permission checks | Bypassed entirely |
| JWT permissions | `[]` empty |
| Scope | Everything |
| Django Admin | Yes |
| Who gets it | 1–2 break-glass accounts only |
| Who can assign | Cannot be assigned via IAM — set directly in DB |

### Rules
- Never assigned through the IAM user management UI
- Reserved for emergency access and initial system setup
- Should not be used for day-to-day operations
- Credentials must be stored securely (password manager, vault)

---

## Tier 1 — `platform.admin`

| Property | Value |
|---|---|
| Scope | All systems, all departments |
| Permission checks | Goes through normal checks |
| JWT permissions | All permission codes embedded |
| Department required | No |
| Django Admin | No |
| Who gets it | Developers, platform managers |
| Who can assign | Superuser only |

### Rules
- Hidden from `dept.admin` — cannot be assigned by department admins
- Does not require a department assignment
- Has full access to all systems and all resources
- Permissions are still checked via JWT (auditable)
- When a new system or resource is added, the `platform.admin` policies must be updated manually

---

## Tier 1 — `platform.viewer`

| Property | Value |
|---|---|
| Scope | All systems, all departments |
| Permission checks | Goes through normal checks |
| JWT permissions | All read permissions embedded |
| Department required | No |
| Django Admin | No |
| Who gets it | Auditors, senior stakeholders |
| Who can assign | Superuser only |

### Rules
- Hidden from `dept.admin`
- Read-only across all systems — no create, update, or delete
- Useful for compliance, monitoring, and reporting roles

---

## Tier 2 — `dept.admin`

| Property | Value |
|---|---|
| Scope | Own department only |
| Permission checks | Goes through normal checks |
| JWT permissions | IAM management permissions embedded |
| Department required | Yes |
| Django Admin | No |
| Who gets it | Department heads, team leads |
| Who can assign | Superuser only |

### Rules
- Can manage users only within their own department
- Cannot modify users with `platform.admin`, `platform.viewer`, or `dept.admin` roles (hidden roles)
- Cannot assign hidden roles to other users
- Cannot move users to another department
- Actor and target must be in the same department
- Actor cannot update their own account

---

## Tier 2 — `dept.viewer`

| Property | Value |
|---|---|
| Scope | Own department only |
| Permission checks | Goes through normal checks |
| JWT permissions | IAM read permissions embedded |
| Department required | Yes |
| Django Admin | No |
| Who gets it | Department supervisors, HR liaisons |
| Who can assign | Superuser only |

### Rules
- Can view users only within their own department
- No create, update, or delete access

---

## Tier 3 — `{system}.admin` / `{system}.viewer`

Examples: `tropos.admin`, `inventory.viewer`, `cmr.admin`

| Property | Value |
|---|---|
| Scope | Specific system only |
| Permission checks | Goes through normal checks |
| JWT permissions | System-specific permissions embedded |
| Department required | Yes (unless global role) |
| Django Admin | No |
| Who gets it | System-specific team members |
| Who can assign | Superuser or `dept.admin` (within department) |

### Rules
- Scoped to a single system — no access to other systems
- `dept.admin` can assign system-specific roles to users within their department
- Viewer variants are read-only within their system
- Admin variants have full CRUD within their system

---

## Role Assignment Rules Summary

| Role | Who can assign |
|---|---|
| `platform.admin` | Superuser only |
| `platform.viewer` | Superuser only |
| `dept.admin` | Superuser only |
| `dept.viewer` | Superuser only |
| `{system}.admin` | Superuser or `dept.admin` (same department) |
| `{system}.viewer` | Superuser or `dept.admin` (same department) |

---

## Hidden Roles

Roles in `HIDDEN_FROM_IAM_ADMIN` cannot be seen or assigned by `dept.admin`:

```python
HIDDEN_FROM_IAM_ADMIN = {
    "platform.admin",
    "platform.viewer",
    "dept.admin",
    "dept.viewer",
}
```

---

## Global Roles

Roles in `GLOBAL_ROLES` do not require a department assignment:

```python
GLOBAL_ROLES = {
    "platform.admin",
    "platform.viewer",
}
```

---

## Frontend Behavior by Role

| Role | Systems shown | Nav items shown |
|---|---|---|
| Superuser | All (`is_superuser: true` → skip filtering) | All |
| `platform.admin` | All (permissions cover all) | All |
| `platform.viewer` | All (read permissions cover all) | All (read-only actions) |
| `dept.admin` | IAM system only | User management within department |
| `{system}.admin` | Their system only | Full system nav |
| `{system}.viewer` | Their system only | Read-only system nav |

---

## Role Code Reference

| Code | Name | Tier |
|---|---|---|
| *(superuser)* | Superuser | 0 |
| `platform.admin` | Platform Admin | 1 |
| `platform.viewer` | Platform Viewer | 1 |
| `dept.admin` | Department Admin | 2 |
| `dept.viewer` | Department Viewer | 2 |
| `tropos.admin` | Tropos Admin | 3 |
| `tropos.viewer` | Tropos Viewer | 3 |
| `inventory.admin` | Inventory Admin | 3 |
| `inventory.viewer` | Inventory Viewer | 3 |
| `cmr.admin` | CMR Admin | 3 |
| `cmr.viewer` | CMR Viewer | 3 |
