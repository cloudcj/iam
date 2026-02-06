# What we need for building our IAM

## What we remove/stop using

#### These are monolith-only concepts.

#### They must not exist in a universal IAM.

- Django Groups

  user.groups  
  request.user.groups.filter(...)

  Why:

  Django-only  
   ORM-dependent  
   Cannot be used by non-Django services  
   Cannot be embedded in JWT  
   👉 Replace with IAM Roles

- Django Permission

  user.has_perm(...)
  django.contrib.auth.models.Permission

  Why:

  Tied to Django models  
  Tied to apps  
  Impossible to version across services  
  👉 Replace with business permissions (inventory.read)

- Session Base Authentication

- Authorization Logic in Models / Managers
  - is_admin
  - is_root
  - exclude(groups\_\_name=...)

  Why:

  Authorization ≠ identity  
  Logic becomes invisible and dangerous  
  👉 Authorization lives in JWT + permission checks

## What We KEEP From Django (On Purpose)

Django is still excellent at some things.

✅ AbstractBaseUser

Why:

Password hashing  
Authentication compatibility  
Minimal identity core

✅ PermissionsMixin (Limited Use)

Why:

Admin compatibility  
is_superuser  
Management commands  
What we don’t use:  
user_permissions  
groups

✅ ModelBackend

Why:

Password verification  
authenticate()  
Admin login  
createsuperuser

This is login only, not authorization.

✅ Django Admin (IAM Only)

Why:

Manage users  
Assign roles  
Audit actions  
Admin ≠ runtime authorization.

## What We BUILD Ourselves (Core IAM)

### A. Custom User Model (Identity Only)

What it does:

- Stores username
- Stores password hash
- Stores account state

What it does NOT do:

- Roles
- Permissions
- Policies
  User = who you are

### B. RBAC (Authorization Brain)

Custom models:

    Permission (inventory.read)
    Role (Admin)
    UserRole (link)

Why:

- Business-level authorization
- Framework-agnostic
- Serializable into JWT
  Authorization = what you can do

### C. JWT (Trust Contract)

JWT contains:

    {
        "sub": "user_id",
        "roles": [...],
        "permissions": [...]
    }

Why:

- Stateless
- Language-agnostic
- Verifiable anywhere
  JWT = proof of identity + authority

### D. CustomAuthentication (DRF)

This replaces:

- Session auth
- ORM lookups in services

What it does:

- Read JWT
- Verify signature
- Attach token claims to request
  request.user = token_payload

#### E. Permission Checks (DRF / Services)

Replace:

    IsRootGroup
    user.has_perm()

With:

    HasPermission("inventory.write")

This works in:

- Django
- FastAPI
- Go
- Node

---

# Order of Implementation (VERY IMPORTANT)

Phase 1 — Identity

✔ Custom User
✔ UserManager
✔ Settings

Phase 2 — Authorization

✔ RBAC models
✔ Seed roles & permissions

Phase 3 — Trust

✔ JWT issuing
✔ JWT verification

Phase 4 — Enforcement

✔ DRF permission classes
✔ Service checks

Phase 5 — Hardening

✔ Refresh tokens
✔ Revocation
✔ Audit logs

## One-Screen Mental Model (Lock This In)

Django
└── Login (password check only)

IAM
└── RBAC (roles + permissions)

JWT
└── Authority contract

Services
└── Verify JWT
└── Enforce permissions

If a service:

- queries IAM DB ❌
- checks Django groups ❌
- calls IAM per request ❌

Your IAM is broken.

---

Final Truth (No Sugarcoating)

You are not “using Django auth” anymore.

You are:

- using Django as an identity engine
- building your own authorization system
- using JWT as the trust boundary
- That’s exactly what real IAM platforms do.

✅ What You Should Do NEXT (Concrete)

Now that the mental model is clear, the correct next step is:

👉 Build the login flow end-to-end

Because:

- it touches identity
- it touches RBAC
- it issues JWT
- it proves everything works
- If you want, next I can:

1️⃣ Build LoginView step-by-step
2️⃣ Build JWT issuing code
3️⃣ Wire RBAC into login

👉 Reply “LOGIN FLOW” and we’ll implement it cleanly.
