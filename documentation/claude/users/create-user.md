# Create User — Form Logic & API Reference

## Overview

The Create User modal (`CreateUserModal.tsx`) allows platform admins and superusers to create a new user with basic info and roles. **Direct permission assignment is not available at creation time** — the user starts with only role-derived permissions. Extra direct permissions can be added later via Edit User.

---

## APIs Used

### On Modal Open (fetched in parallel)

| Hook | Endpoint | Purpose |
|---|---|---|
| `useGetMeQuery()` | `GET /api/v1/me/` | Determine actor role (superuser / platform admin / dept admin) |
| `useGetDepartmentsQuery()` | `GET /api/v1/department/` | Populate department dropdown |

### When Department is Selected

| Hook | Endpoint | Purpose |
|---|---|---|
| `useGetRoleFormOptionsQuery(departmentId)` | `GET /api/v1/access/roles/form-options/?department=:id` | Returns available management roles + system roles scoped to that department, with their policies and `grants_systems` |

### On Save

| Hook | Endpoint | Payload |
|---|---|---|
| `useCreateUserMutation()` | `POST /api/v1/identity/users/create/` | `{ username, password, first_name, last_name, email, department, roles: [...roleIds] }` |

> No `permission_ids` is sent at creation. Permissions are derived entirely from roles by the backend.

---

## State

```typescript
const [managementRole, setManagementRole] = useState<string | null>(null)
const [systemRoles, setSystemRoles] = useState<Record<string, string>>({})
```

| State | Type | Description |
|---|---|---|
| `managementRole` | `string \| null` | Selected management role **code** (e.g. `"department.admin"`) |
| `systemRoles` | `Record<string, string>` | Map of `{ system: roleId }` (e.g. `{ tropos: "uuid-123" }`) |

No permission state — the form does not manage direct permissions.

---

## Form Fields

| Field | Required | Notes |
|---|---|---|
| `username` | Yes | Must be unique |
| `password` | Yes | Min 8 characters |
| `first_name` | Yes | |
| `last_name` | Yes | |
| `email` | Yes | Must be unique |
| `department` | Yes (superuser/platform admin) | Auto-set for dept admin |

---

## Role Selection Flow

### 1. Department Selected
Triggers `useGetRoleFormOptionsQuery(departmentId)` — fetches roles scoped to the department.

### 2. Management Role Selected
```typescript
// Role with grants_systems (e.g. department.admin grants tropos, ghidora)
→ auto-selects matching system roles using admin/viewer suffix:
    tropos.admin  if role ends with ".admin"
    tropos.viewer if role ends with ".viewer"

// Role cleared
→ systemRoles reset to {}
```

### 3. System Roles
Each system in `allowedSystems` gets its own dropdown. The actor can override the auto-selected role or pick manually.

```typescript
// allowedSystems is determined by:
grants_systems from managementRole  (if present)
selectedDept.allowed_systems        (fallback)
```

---

## Policy Preview

Once roles are selected, the form shows a **read-only policy preview** (`PolicyCard`) listing which policies will be granted:

```typescript
// Deduplicates policies from all selected roles
const resolvedPolicies = [
  ...selectedMgmtRole.policies,         // shown in blue
  ...systemRoles[each].policies,        // shown in teal
]
```

This gives the actor visibility into what permissions the user will receive before submitting. The note under the list reads: *"These policies are auto-assigned from selected roles and cannot be changed at creation."*

---

## Actor Restrictions

| Actor | Department | Can assign management role | Can assign system roles |
|---|---|---|---|
| Superuser | Any | `platform.*` + `department.*` | All |
| Platform Admin | Any | `department.*` only | All in dept's allowed systems |
| Dept Admin | Own dept (fixed) | None | Only in their dept's allowed systems |

---

## On Save

```typescript
await createUser({
  username, password, first_name, last_name, email,
  department: deptId,
  roles: [...managementRoleId, ...systemRoleIds],
  // no permission_ids
})
```

The backend (`create_user` service) derives `SOURCE_ROLE` permissions automatically from the submitted roles. No `SOURCE_DIRECT` permissions are created at this point.

---

## Full Flow

```
useGetMeQuery()
    → actor is platform.admin
    → isDeptAdmin = false  (department dropdown shown)

useGetDepartmentsQuery()
    → populates department Select

Department selected
    → useGetRoleFormOptionsQuery(deptId) fires
    → returns management_roles + system_roles scoped to dept

Management role selected
    → auto-selects system roles (admin/viewer suffix)
    → resolvedPolicies recomputes  →  PolicyCard preview updates

On save
    → POST sends roles[] only
    → backend derives SOURCE_ROLE permissions from roles
    → no direct permissions created
```

---

## Difference from Edit User

| Feature | Create | Edit |
|---|---|---|
| Username field | Editable | Only superuser can edit |
| Password field | Required | Not shown (use Reset Password) |
| Permission checkboxes | Not shown | Shown for superuser / platform admin |
| Direct permission assignment | No | Yes |
| Init data from server | None needed | Loads `userDetail` for existing perms |
