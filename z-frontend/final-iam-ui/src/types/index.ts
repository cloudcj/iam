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
  } | null
  roles: string[]
}

export interface UserDetail {
  id: string
  username: string
  first_name: string
  last_name: string
  email: string
  is_active: boolean
  department: string | null
  roles: string[]
  permission_codes: string[]
  extra_permission_ids: string[]  // source=direct permission IDs
}


export interface UpdateUserPayload {
  username?: string
  first_name: string
  last_name: string
  email: string
  department: string
  roles: string[]
  permission_ids?: string[]
}



export interface CreateUserPayload {
  username: string
  password: string
  email?: string
  first_name: string
  last_name: string
  department?: string   // UUID
  roles: string[]       // UUID[]
  permissions?: string[]
}




export interface Permission {
  id: string
  code: string
  system: string
  resource: string
  action: string
  description: string
}


export interface Me {
  id: string
  username: string
  email: string
  first_name: string
  last_name: string
  is_superuser: boolean
  department: {
    code: string
    name: string
  }
  systems: string[]
  permissions: string[]   // ← permission codes, not roles
}


export interface LoginRequest {
  username: string
  password: string
}

// Department
export interface Department {
  id: string
  code: string
  name: string
  allowed_systems: string[]  // e.g. ["tropos", "ghidora"]
}

// Role
export interface Role {
  id: string
  code: string
  name: string
  system: string
  policies: Policy[]
}

// Policy
export interface Policy {
  id: string
  code: string
  name: string
  system: string
  resource: string
  description: string
  permission_codes: string[]
}

