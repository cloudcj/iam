
PHASE 1: Foundation
1.) Create core models
2.) Bootstrap users/ Seed core data

PHASE 2: USER LIFECYCLE (ADMIN SIDE)
1.) User creation (NO JWT YET) - create user, assign department, assign role
2.) Role Assignment (WITH VALIDATION) - UserDepartment : DepartmentAllowedRole - assignments.py (service layer)

PHASE 3 — AUTHENTICATION (LOGIN)
1.) User Login (AuthN) - this is where jwt should be handled
2.) Resolve Roles - Permissions (AuthZ)
3.) Create JWT (CRITICAL) - JWT is issued after permission resolution

PHASE 4 — REQUEST AUTHORIZATION (RUNTIME)
1.) CustomAuthentication (EVERY REQUEST)
2.) Permission Enforcement (EVERY REQUEST)

PHASE 5 — CHANGES & REFRESH
1.) Role / Permission Changes


summary:

BOOTSTRAP:
Create departments, roles, permissions

ADMIN:
Create user
→ assign department
→ assign role (validated)

LOGIN:
Authenticate user
→ resolve permissions
→ issue JWT

REQUEST:
Validate JWT
→ check permission
→ allow / deny




=====================================================================================================
=====================================================================================================

🧱 PHASE 1 — FOUNDATION (DO THIS FIRST)
✅ Step 1: Create Core Models

You already did this ✔

Create models for:

User
Department
Permission
Role
RolePermission
UserDepartment
DepartmentAllowedRole
UserRole

📌 No JWT yet
📌 No permissions checking yet

✅ Step 2: Bootstrap / Seed Core Data

Before users can do anything, the system must exist.

Create:

Departments (INVENTORY, PLATFORM, SECURITY)
Permissions (inventory.read, iam.user.create, etc.)
Roles (InventoryViewer, PlatformAdmin)
Role → Permission mappings
Department → Allowed Roles mappings
One super admin user

👉 This is non-negotiable for IAM.

👤 PHASE 2 — USER LIFECYCLE (ADMIN SIDE)
✅ Step 3: User Creation (NO JWT YET)

Who does this?

Admin
Bootstrap process
HR / provisioning system

What happens

Create User
→ Assign Department(s)
→ (Optional) Assign initial Role(s)


📌 Still no JWT
📌 Still no permissions resolution

✅ Step 4: Role Assignment (WITH VALIDATION)

When assigning a role:

UserDepartment ∩ DepartmentAllowedRole


If invalid → ❌ reject assignment

📌 This happens:

In admin APIs

In service layer (assignments.py)

📌 This does NOT:

Generate JWT

Resolve permissions

🔐 PHASE 3 — AUTHENTICATION (LOGIN)
✅ Step 5: User Login (AuthN)

This is the FIRST time JWT appears

Flow:

Username + Password
→ Authenticate credentials
→ User identity confirmed


At this point:
✔ You know who the user is
❌ You don’t yet know what they can do

✅ Step 6: Resolve Roles → Permissions (AuthZ)

Now call:

roles, permissions = resolve_user_roles_and_permissions(user)


This:

Reads DB

Resolves assigned roles

Produces flat permission list

📌 Happens ONLY:

On login

On token refresh

✅ Step 7: Create JWT (CRITICAL)

Now build the JWT:

{
  "sub": "user_id",
  "username": "alice",
  "permissions": [
    "inventory.read",
    "inventory.write"
  ],
  "iat": 1700000000,
  "exp": 1700003600
}


📌 JWT is issued after permission resolution
📌 JWT is now your authorization contract

🌐 PHASE 4 — REQUEST AUTHORIZATION (RUNTIME)
✅ Step 8: CustomAuthentication (EVERY REQUEST)

On every API call:

Authorization: Bearer <JWT>


Your CustomAuthentication:

Validates token

Loads user

Sets:

request.user

request.auth (JWT claims)

📌 No DB permission queries here

✅ Step 9: Permission Enforcement (EVERY REQUEST)

Your HasPermission runs:

required_permission = "inventory.read"


Checks:

required_permission ∈ request.auth.permissions


✔ Allow → controller executes
❌ Deny → 403 Forbidden

🔄 PHASE 5 — CHANGES & REFRESH
✅ Step 10: Role / Permission Changes

When admin:

Assigns new role

Removes role

Changes permissions

👉 Existing JWTs are now stale

You must:

Force logout

OR rely on short-lived tokens

OR refresh token flow

📌 This is why refresh tokens exist

🧠 ONE-PAGE SUMMARY (MEMORIZE THIS)
BOOTSTRAP:
Create departments, roles, permissions

ADMIN:
Create user
→ assign department
→ assign role (validated)

LOGIN:
Authenticate user
→ resolve permissions
→ issue JWT

REQUEST:
Validate JWT
→ check permission
→ allow / deny

🏁 Answer to Your Core Question

No, JWT is NOT created during user creation.
JWT is created only during login (authentication).

User creation and role assignment are admin workflows.
JWT creation is a runtime auth workflow.

✅ What You Should Code NEXT (VERY CLEAR)

👉 Implement Step 5–7:

Login endpoint

Call resolve_user_roles_and_permissions

Issue JWT with permissions

If you want, next I can:

Write the login API

Show JWT creation code

Review your CustomAuthentication

Add refresh token strategy

Draw this as an ASCII diagram for docs










=========================================================================================================================================
=========================================================================================================================================
=========================================================================================================================================
=========================================================================================================================================

# GAIA IAM — Identity & Access Management Service

GAIA IAM is a **standalone Identity and Access Management (IAM) service** designed for a **microservices architecture**.  
It provides **authentication**, **authorization**, and **token issuance** for all Gaia services.

This IAM is **framework-agnostic at the protocol level** and acts as the **single source of truth** for identity.

---

## 🎯 Goals

- Centralize authentication and authorization
- Support microservices without shared databases
- Eliminate per-request IAM calls
- Use modern, secure token-based authentication
- Be reproducible, auditable, and production-ready

---

## 🧱 Core Design Decisions

| Area                | Decision                                 |
| ------------------- | ---------------------------------------- |
| Backend             | Django + Django REST Framework           |
| Auth mechanism      | JWT                                      |
| JWT signing         | RS256 (asymmetric keys)                  |
| Authorization model | RBAC (Role-Based Access Control)         |
| Token type          | Short-lived access token + refresh token |
| IAM role            | Authority only (no business logic)       |
| Service behavior    | Trust JWT, never query IAM DB            |

---

## 🧠 High-Level Architecture

- IAM issues signed tokens
- Services verify tokens using IAM public key
- No service-to-IAM calls per request
- No shared databases

---

## 🧩 Step-by-Step Build Overview

### STEP 0 — Foundational Rules

- IAM is a **standalone service**
- Other services **never manage users**
- Tokens are **contracts**
- Authorization is **data-driven**, not hardcoded

---

### STEP 1 — Custom User Model (Identity)

Purpose:

- Represent users and system identities
- Securely manage credentials

Key points:

- Uses Django’s authentication base for password hashing
- Login via `username`
- Email is optional metadata
- UUID primary key
- Designed to be independent of Django permissions

Result:

- Secure identity layer
- Framework-independent user representation

---

### STEP 2 — RBAC Model (Authorization)

Purpose:

- Define _what actions are allowed_

Entities:

- **Permission** — atomic action (e.g. `inventory.read`)
- **Role** — business grouping (e.g. `Admin`)
- **UserRole** — explicit mapping between users and roles

Key principles:

- UUID everywhere
- No Django `Group`
- No Django `auth_permission`
- Explicit, portable RBAC model

Result:

- Clean and scalable authorization system

---

### STEP 3 — RBAC Seeder (Source of Truth)

Purpose:

- Make IAM deterministic and reproducible

Key ideas:

- Roles and permissions are defined in code
- Seeder is idempotent
- No manual admin setup
- Same RBAC across all environments

Result:

- CI/CD-friendly IAM
- No configuration drift

---

### STEP 4 — Login Flow (Authentication)

Purpose:

- Verify user credentials
- Issue signed tokens

Flow:

1. User submits username and password
2. Django verifies password hash
3. IAM loads roles and permissions
4. IAM generates a JWT payload
5. IAM signs the JWT using private key

Result:

- Stateless, signed access token

---

### STEP 5 — Access Token (JWT)

Purpose:

- Prove identity and authorization to services

Characteristics:

- Short-lived (e.g. 15 minutes)
- Contains:
  - user ID
  - username
  - roles
  - permissions
- Signed with RS256
- Verified using public key

Result:

- Services can trust tokens without DB access

---

### STEP 6 — JWT Verification (Authentication Layer)

Purpose:

- Validate incoming requests

Process:

- Extract JWT from request
- Verify signature and expiration
- Validate issuer
- Attach claims to request context

Result:

- Request is authenticated
- Identity data is available to the service

---

### STEP 7 — Permission Enforcement (Authorization Layer)

Purpose:

- Enforce access control

Key ideas:

- Views declare required permissions
- Permissions are checked against JWT claims
- No DB queries
- No IAM calls

Result:

- Fast and consistent authorization

---

### STEP 8 — Refresh Tokens (Session Management)

Purpose:

- Maintain sessions without re-login
- Improve security

Design:

- Access tokens are stateless and short-lived
- Refresh tokens are stored in the database
- Refresh tokens are rotated on every use
- Old refresh tokens are revoked

Flow:

1. Access token expires
2. Client sends refresh token
3. IAM validates and rotates refresh token
4. New access token is issued

Result:

- Secure long-lived sessions
- Replay attack protection

---

### STEP 9 — Token Transport Strategy

Different clients use different delivery mechanisms:

| Client Type    | Token Transport  |
| -------------- | ---------------- |
| Browser apps   | HttpOnly cookies |
| Postman / APIs | Bearer token     |
| Microservices  | Bearer token     |

Important:

- JWT structure stays the same
- Only transport mechanism changes

---

### STEP 10 — Trust Model (Microservices)

Rules:

- Services trust IAM public key
- Services never call IAM per request
- Services never share secrets
- Tokens are the trust boundary

Result:

- Zero-trust internal architecture
- Horizontally scalable platform

---

### STEP 11 — Security Guarantees

- Private key never exposed
- Public key can be shared safely
- Tokens expire
- Refresh tokens rotate
- Permissions are immutable per token lifetime

---

## 🧠 Mental Model

No shared DB.  
No synchronous IAM dependency.  
No hidden state.

---

## ✅ Current Status

GAIA IAM currently supports:

- Custom user authentication
- UUID-based RBAC
- Deterministic RBAC seeding
- JWT access tokens (RS256)
- Refresh token rotation
- Stateless authorization

This is **enterprise-grade IAM**.

---

## 🚀 Next Enhancements

Planned extensions include:

- Cookie-based JWT for frontend
- Service-to-service authentication
- Logout & token revocation
- JWKS endpoint & key rotation
- API gateway integration (NGINX)

---

## 📌 Summary

GAIA IAM is designed to be:

- Secure
- Stateless
- Scalable
- Auditable
- Framework-agnostic

It acts as the **single authority for identity and access** across the Gaia platform.
