Final-IAM is a Django-based Identity & Access Management (IAM) service with JWT authentication (RS256), role-based access control (RBAC) with permission-level enforcement, department-scoped multi-tenancy, and a React admin frontend.

What's Been Built
Backend (Django / DRF)
Authentication (apps/authn/)

Login/logout with HttpOnly JWT cookies (RS256, 15 min access / rotating refresh)
Dual auth: cookie (browser) + Authorization: Bearer header (M2M)
Redis-backed refresh token blacklisting
CSRF endpoint for browser clients
JWKS endpoint (apps/jwks/) for RS256 public key discovery
Authorization (apps/authz/)

HasPermission DRF permission class — checks view.required_permission against JWT permissions[] claim (no DB hit at request time)
resolve_user_effective_permissions() — computes permissions from UserRole → Role → RolePermission chain
Access Control (apps/access/)

Models: Role, Policy, Permission, UserRole, UserPolicy, RolePolicy, RolePermission
PBAC architecture: User → Role → Policy → Permission → JWT
UserPolicy is source of truth for permissions; UserRole is for visibility/management only
DepartmentAllowedSystem — restricts which systems a department can access
DepartmentAllowedRole — restricts which roles can be assigned within a department
Identity / User Management (apps/identity/)

Custom User model (UUID PK, department FK)
Full CRUD: create, list (paginated), detail, update, delete (soft deactivate), reset password
Actor-scoped operations: superuser > platform admin > dept admin each have different visibility and assignment rules
CustomPagination — uniform { page, per_page, num_pages, count, next, previous, results } shape
Department Management (apps/department/)

CRUD for departments with allowed system scoping
Audit Logging (apps/audit/)

Logs actor, action, target, status, IP, timestamp
Seeder (seeder/)

Seeds in order: permissions → policies → roles → departments → superadmin
Idempotent (get_or_create pattern)
Frontend (React + Mantine + RTK Query)
IAM Admin Pages (src/pages/)

DashboardPage — total users, active users counts
UsersPage — paginated user table, search, filter by status/department/role, create/view/edit/delete actions, permission-gated buttons
DepartmentsPage — list, create, edit departments
RolesPage — list roles with policies
PermissionsPage — list all permissions
AuditLogPage — filterable audit log viewer
ProfilePage — current user profile + password change
User Modals (src/components/users/)

CreateUserModal — username, password, email, department, role selection, policy preview
EditUserModal — role/permission management with directPermIds vs rolePermIds separation; role change clears direct permissions (intentional UX)
ViewUserModal — read-only user detail
ResetPasswordModal — password reset
Tropos Pages (src/pages/tropos/)

TroposDashboardPage
Infrastructure: RegionsPage, RacksPage
Assets: DevicesPage, ServersPage, SwitchesPage, AppliancesPage
UsersPage — reads from IAM (Tropos has no local user store)
State / API (src/services/)

iamApi (RTK Query) — users, me, departments, roles, permissions, audit logs
inventoryApi (RTK Query) — Tropos inventory resources
Architecture Model

User → Role → Policy → Permission → JWT claims
                                  ↓
                         HasPermission (no DB hit)
Actor Permission Hierarchy
Actor	Can See	Can Assign
Superuser	All users	Any role, direct permissions
Platform Admin	All users	System roles (not platform.admin), no direct perms
Dept Admin	Own dept only (excludes hidden roles)	System roles scoped to dept's allowed systems