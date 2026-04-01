# Create User

## Overview

Creates a new user with basic info and roles. Direct permission assignment is not available at creation — the user starts with only role-derived permissions. Extra direct permissions can be added later via Edit User.

**Frontend:** `CreateUserModal.tsx`  
**Permission required:** `iam.user.create` or superuser

---

## API Reference

### Create User

```
POST /api/v1/identity/users/create/
```

**Auth:** JWT cookie or `Authorization: Bearer <token>`  
**Permission:** `iam.user.create` or superuser

#### Request Body

```json
{
  "username": "jdoe",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe",
  "email": "jdoe@example.com",
  "department": "uuid",
  "roles": ["uuid", "uuid"]
}
```

#### Request Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `username` | string | Yes | Must be unique |
| `password` | string | Yes | Min 8 characters |
| `first_name` | string | Yes | |
| `last_name` | string | Yes | |
| `email` | string | No | Must be unique if provided |
| `department` | UUID | Yes (superuser / platform admin) | Auto-set to actor's dept for dept admin |
| `roles` | UUID[] | Yes | At least one role required |

> `permission_ids` is not accepted at creation. Permissions are derived from roles by the backend automatically.

#### Response `201 Created`

```json
{
  "id": "uuid",
  "username": "jdoe",
  "email": "jdoe@example.com",
  "department": {
    "id": "uuid",
    "code": "CLOUD_PLATFORM",
    "name": "Cloud Platform"
  }
}
```

#### Error Responses

| Status | Reason |
|---|---|
| `400` | Validation error (missing fields, duplicate username/email) |
| `403` | Actor lacks `iam.user.create` permission, or tried to assign a restricted role |

---

### Supporting Endpoints (used by the form)

#### Get Departments
```
GET /api/v1/department/
```
Populates the department dropdown.

#### Get Role Form Options
```
GET /api/v1/access/roles/form-options/?department=<uuid>
```
Returns management roles and system roles scoped to the selected department, including their policies and `grants_systems`.

```json
{
  "management_roles": [
    {
      "id": "uuid",
      "code": "department.admin",
      "name": "Department Admin",
      "system": "iam",
      "grants_systems": ["tropos"],
      "policies": [...]
    }
  ],
  "system_roles": {
    "tropos": [
      { "id": "uuid", "code": "tropos.admin", "name": "Tropos Admin", ... }
    ]
  }
}
```

---

## Actor Restrictions

| Actor | Department | Can assign management role | Can assign system roles |
|---|---|---|---|
| Superuser | Any | `platform.*` + `department.*` | All |
| Platform Admin | Any | `department.*` only | All in dept's allowed systems |
| Dept Admin | Own dept (fixed) | None | Only in their dept's allowed systems |

---

## Backend Reference

### Service (`apps/identity/services/user/create.py`)

`create_user()` performs:
1. Validates actor permissions for the requested roles
2. Resolves `department` — required for superuser/platform admin, auto-set for dept admin
3. Creates the `User` record
4. Bulk-creates `UserRole` entries (visibility/management)
5. Bulk-creates `UserPermission` entries with `source=SOURCE_ROLE` (derived from roles)

No `SOURCE_DIRECT` permissions are created at this point.

### Serializer (`apps/identity/serializers/user/create.py`)

```python
username      = CharField()
password      = CharField(write_only=True)
first_name    = CharField()
last_name     = CharField()
email         = EmailField(required=False)
department    = UUIDField(required=False)
roles         = ListField(child=UUIDField(), required=True, allow_empty=False)
```

### Audit Log

On success, logs `user.create` with `detail: { "username": "<username>" }`.

---

## Frontend Reference

### RTK Query Hooks

| Hook | Endpoint | When |
|---|---|---|
| `useGetMeQuery()` | `GET /api/v1/me/` | On mount — determines actor role |
| `useGetDepartmentsQuery()` | `GET /api/v1/department/` | On mount — populates department dropdown |
| `useGetRoleFormOptionsQuery(deptId)` | `GET /api/v1/access/roles/form-options/?department=:id` | When department is selected |
| `useCreateUserMutation()` | `POST /api/v1/identity/users/create/` | On save |

### State

```typescript
const [managementRole, setManagementRole] = useState<string | null>(null)
const [systemRoles, setSystemRoles] = useState<Record<string, string>>({})
```

| State | Type | Description |
|---|---|---|
| `managementRole` | `string \| null` | Selected management role code |
| `systemRoles` | `Record<string, string>` | `{ system: roleId }` — one role per system |

No permission state — the form does not manage direct permissions.

### Role Selection Flow

1. **Department selected** → fires `useGetRoleFormOptionsQuery(deptId)`
2. **Management role selected** → auto-selects system roles using admin/viewer suffix matching
3. **Management role cleared** → `systemRoles` reset to `{}`
4. **System roles** → each allowed system gets its own dropdown, actor can override

`allowedSystems` is determined by `grants_systems` from the management role (or `department.allowed_systems` as fallback).

### Policy Preview

Once roles are selected, a read-only `PolicyCard` shows which policies will be granted — deduped across all selected roles. Gives the actor visibility before submitting.

### On Save

```typescript
await createUser({
  username, password, first_name, last_name, email,
  department: deptId,
  roles: [...managementRoleId, ...systemRoleIds],
})
```

---

## Comparison with Edit User

| Feature | Create | Edit |
|---|---|---|
| Username field | Editable | Superuser only |
| Password field | Required | Not shown (use Reset Password) |
| Permission checkboxes | Not shown | Shown for superuser / platform admin |
| Direct permission assignment | No | Yes |
| Init data from server | None | Loads `userDetail` for existing perms |
