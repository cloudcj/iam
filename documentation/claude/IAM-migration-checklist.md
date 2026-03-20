# IAM Migration Checklist

This document tracks all changes needed based on the role hierarchy redesign and PBAC (Policy-Based Access Control) decisions.

---

## Registry

### Roles — Rename to tier-based naming
| Old Code | New Code | Tier |
|---|---|---|
| `global.admin` | `platform.admin` | 1 |
| `global.readonly` | `platform.viewer` | 1 |
| `iam.admin` | `dept.admin` | 2 |
| `iam.viewer` | `dept.viewer` | 2 |

- [ ] `registry/roles/global_roles.py` — rename roles, add `platform.admin`, have both reference system policies directly
- [ ] `registry/roles/iam.py` — rename `iam.admin` → `dept.admin`, `iam.viewer` → `dept.viewer`
- [ ] `registry/roles/inventory.py` — no changes needed (tier 3 names are correct)

### Global Policies
- [ ] `registry/policies/global_policies.py` — remove or clean up, no longer needed. Global roles reference system policies directly.

### System Registries — Item-level resources
Instead of coarse resources (e.g. `infrastructure`, `asset`), use item-level resources so nav filtering is granular.

- [ ] Update each system registry to define per-item resources:

Example for Tropos:
```python
# Before (coarse)
"infrastructure": ("Infrastructure", ["read", "create", "update", "delete"])

# After (item-level)
"az":       ("Availability Zones", ["read", "create", "update", "delete"]),
"room":     ("Rooms",              ["read", "create", "update", "delete"]),
"pod":      ("Pods",               ["read", "create", "update", "delete"]),
"rack":     ("Racks",              ["read", "create", "update", "delete"]),
"device":   ("Devices",            ["read", "create", "update", "delete"]),
"server":   ("Servers",            ["read", "create", "update", "delete"]),
"switch":   ("Switches",           ["read", "create", "update", "delete"]),
"appliance":("Appliances",         ["read", "create", "update", "delete"]),
```

---

## Constants

- [ ] `apps/common/constants/role_codes.py` — update to new role code names:
```python
class RoleCodes:
    PLATFORM_ADMIN   = "platform.admin"
    PLATFORM_VIEWER  = "platform.viewer"
    DEPT_ADMIN       = "dept.admin"
    DEPT_VIEWER      = "dept.viewer"
    INVENTORY_VIEWER = "inventory.viewer"
    INVENTORY_ADMIN  = "inventory.admin"
```

- [ ] `apps/common/constants/hidden_constants.py` — update with new codes:
```python
HIDDEN_FROM_IAM_ADMIN = {
    RoleCodes.PLATFORM_ADMIN,
    RoleCodes.PLATFORM_VIEWER,
    RoleCodes.DEPT_ADMIN,
    RoleCodes.DEPT_VIEWER,
}
```

- [ ] `apps/common/constants/global_role_constants.py` — update:
```python
GLOBAL_ROLES = {
    RoleCodes.PLATFORM_ADMIN,
    RoleCodes.PLATFORM_VIEWER,
}
```

---

## Models

- [ ] Verify `UserRole` model exists — used for management/visibility control
- [ ] Verify `UserPolicy` model exists — used for permission resolution (source of truth)

`UserPolicy` should look like:
```python
class UserPolicy(models.Model):
    user   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_policies")
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "policy")
```

---

## Services

### Permission Resolution
- [ ] `get_user_permission_codes` — must union both sources:
```python
# From UserRole → Role → Policies → Permissions
role_permissions = ...

# From UserPolicy → Policy → Permissions (direct/temporary assignments)
direct_permissions = ...

# Final
return role_permissions | direct_permissions
```

### User Creation
- [ ] Build/update user creation service with actor-based rules:

| Actor | Department | Role assignment | Policy assignment |
|---|---|---|---|
| Superuser | Any including global | Any role | Any policy |
| Platform Admin | Any including global | Any except `platform.admin` | Any policy |
| Dept Admin | Own dept only (auto-set) | Tier 3 roles only | Own dept scope only |

### User Visibility
- [ ] Build `get_visible_users` service:

| Actor | Can see |
|---|---|
| Superuser | All users |
| Platform Admin | All users |
| Dept Admin | Own dept users excluding hidden role users |

```python
def get_visible_users(*, actor):
    if actor.is_superuser:
        return User.objects.all()
    if has_role(actor, RoleCodes.PLATFORM_ADMIN):
        return User.objects.all()
    if has_role(actor, RoleCodes.DEPT_ADMIN):
        return (
            User.objects
            .filter(department=actor.department)
            .exclude(user_roles__role__code__in=HIDDEN_FROM_IAM_ADMIN)
        )
    return User.objects.none()
```

---

## Seeder

- [ ] Update all role code references in seeder to new names
- [ ] Add `platform.admin` and `platform.viewer` to seed data
- [ ] Ensure seeder order is correct:
  1. Permissions
  2. Policies
  3. Roles
  4. Departments
  5. Superadmin

---

## Documentation

- [ ] `documentation/claude/IAM-roles.md` — update if any rules changed
- [ ] `documentation/claude/IAM-user_creation.md` — update if any rules changed

---

## Key Design Decisions (for reference)

### Roles vs Policies
- **Roles** = presets/convenience for UI, management layer (who can see/manage users)
- **Policies** = source of truth for permissions (what a user can access in systems)
- **UserRole** = controls visibility and management rules in IAM tables
- **UserPolicy** = controls feature access, embedded in JWT

### Hidden Roles
Roles in `HIDDEN_FROM_IAM_ADMIN` cannot be seen, assigned, or modified by `dept.admin`:
- `platform.admin`
- `platform.viewer`
- `dept.admin`
- `dept.viewer`

### Global Roles
Roles in `GLOBAL_ROLES` do not require a department assignment:
- `platform.admin`
- `platform.viewer`

### Superuser vs Platform Admin
- Superuser bypasses all checks, has Django admin, cannot be assigned via UI
- Platform Admin goes through checks, is auditable, can be revoked via IAM UI
- Only superuser can create `platform.admin` accounts
- If a new system is added, superuser auto-has access, platform admin must be updated manually
