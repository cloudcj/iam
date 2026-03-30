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
  permission_codes: string[]
  permission_ids: string[]
  extra_permission_ids: string[]
}

export interface UserListParams {
  search?: string
  is_active?: boolean
  department?: string
  role?: string
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
  roles: string[]         // role codes e.g. ["platform.admin", "tropos.admin"]
  department: {
    id: string
    code: string
    name: string
  }
  systems: string[]
  permissions: string[]   // permission codes
}

// ─── Auth ────────────────────────────────────────────────────────────────────

export interface LoginRequest {
  username: string
  password: string
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
