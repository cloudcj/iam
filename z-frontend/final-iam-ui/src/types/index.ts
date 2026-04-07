// ─── User ────────────────────────────────────────────────────────────────────

export interface RoleRef {
  id: string
  code: string
  name: string
  system: string
  grants_systems?: string[]   // only present on management roles
  policies?: Policy[]         // included in form-options response
}

export interface RoleFormOptions {
  management_roles: RoleRef[]
  system_roles: Record<string, RoleRef[]>
}

export interface User {
  id: string
  username: string
  first_name: string
  last_name: string
  email: string
  is_active: boolean
  department: {
    id: string
    code: string
    name: string
  }
  management_role: RoleRef | null
  system_roles: RoleRef[]
}

export interface UserDetail extends User {
  permission_ids: string[]
  role_permission_ids: string[]
  direct_permission_ids: string[]
}

export interface UserListParams {
  page?: number
  search?: string
  is_active?: boolean
  department?: string
  roles?: string[]
}

export interface PaginatedUsers {
  page: number
  per_page: number
  num_pages: number
  count: number
  next: string | null
  previous: string | null
  results: User[]
}

interface UserBasePayload {
  first_name: string
  last_name: string
  email: string
  roles: string[]   // UUID[]
}

export interface CreateUserPayload extends UserBasePayload {
  username: string
  password: string
  department: string   // UUID — always resolved before sending
}

export interface UpdateUserPayload extends UserBasePayload {
  username?: string         // superuser only
  is_active?: boolean
  department: string        // UUID — always required on update
  permission_ids?: string[] // UUID[] — superuser/platform admin only
}


// ─── Me ──────────────────────────────────────────────────────────────────────

export interface Me {
  id: string
  username: string
  email: string
  first_name: string
  last_name: string
  is_superuser: boolean
  must_change_password: boolean
  roles: string[]         // role codes e.g. ["platform.admin", "tropos.admin"]
  department: {
    id: string
    code: string
    name: string
  }
  systems: string[]
  permissions: string[]   // permission codes
}

export interface LoginResponse {
  detail: string
  must_change_password: boolean
}

// ─── Auth ────────────────────────────────────────────────────────────────────

export interface LoginRequest {
  username: string
  password: string
  recaptcha_token: string
}

// ─── Department ──────────────────────────────────────────────────────────────

export interface Department {
  id: string
  code: string
  name: string
  allowed_systems: string[]   // e.g. ["tropos", "ghidora"]
}

// ─── Access ──────────────────────────────────────────────────────────────────

export interface Role {
  id: string
  code: string
  name: string
  system: string
  policies: Policy[]
}

export interface Policy {
  id: string
  code: string
  name: string
  system: string
  resource: string
  description?: string
  permission_codes: string[]
}

export interface Permission {
  id: string
  code: string
  system: string
  resource: string
  action: string
  description?: string
}

// ─── Audit ───────────────────────────────────────────────────────────────────

export interface AuditLog {
  id: string
  actor: string | null
  actor_name: string | null
  department: string | null
  action: string
  target_id: string | null
  target_type: string
  status: "success" | "failure"
  detail: Record<string, any>
  ip_address: string | null
  timestamp: string
}

export interface AuditLogParams {
  action?: string
  action_category?: string
  status?: string
  target_type?: string
  date_from?: string
  date_to?: string
  limit?: number
  offset?: number
}

export interface AuditLogResponse {
  count: number
  results: AuditLog[]
}

// ─── Dashboard ───────────────────────────────────────────────────────────────

export interface DashboardStats {
  total_users: number
  active_users: number
  inactive_users: number
  total_departments: number
}

export interface UserByDepartment {
  name: string
  user_count: number
}

export interface TopActor {
  username: string
  name: string
  event_count: number
}

export interface RecentActivityLog {
  id: string
  actor: string | null
  actor_name: string | null
  action: string
  status: "success" | "failure"
  ip_address: string | null
  timestamp: string
}

export interface AdminActionLog {
  id: string
  actor: string | null
  actor_name: string | null
  action: string
  target_type: string
  status: "success" | "failure"
  timestamp: string
}

export interface DashboardSummary {
  stats: DashboardStats
  users_by_department: UserByDepartment[]
  failed_logins_7d: number
  login_success_7d: number
  recent_activity: RecentActivityLog[]
  top_actors: TopActor[]
  recent_admin_actions: AdminActionLog[]
}
