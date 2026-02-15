# 🔷 High-Level Implementation Plan

We will build this in 6 structured phases.

## PHASE 1 — Confirm Final Data Rules

Before writing code, we lock behavioral rules:

### 1️⃣ Creation Authority

- Only users with iam.user.create OR is_superuser
- Superuser bypasses all scope checks

### 2️⃣ Department Rule

- Superuser → can set department
- Admin → department auto = actor.department
- Admin cannot change department

### 3️⃣ Role Rule

- Roles optional
- Selected roles must be subset of department.allowed_roles (unless superuser)

### 4️⃣ Policy Rule

- Must have at least one effective policy
- Policies must be subset of:

    union(policy of department.allowed_roles)

- Superuser bypasses scope restriction

### 5️⃣ Flattening Rule

When saving:

    final_policies = (policies_from_roles ∪ manually_selected_policies)

Store only UserPolicy.

Roles stored optionally for reporting.

Runtime will ignore roles.

### 6️⃣ Soft Delete Rule

- Creation unaffected
- Deactivation sets deactivated_at
- Cron handles permanent delete

## 🧱 PHASE 2 — Create Service Layer Structure

We will create:

    identity/
    └── services/
        ├── user_creation_service.py
        ├── user_scope_validator.py
        └── policy_expander.py

Separation of concerns:

    File	                   |           Responsibility
    user_creation_service	   |             orchestration
    user_scope_validator	   |     department + role + policy validation
    policy_expander	           |             expand roles → policies

No validation logic inside serializer.

## 🧱 PHASE 3 — DTO / Input Normalization

We define a clean input structure:

    CreateUserDTO:
        username
        email
        department_id (optional for admin)
        role_ids
        policy_ids

Serializer will only validate data types.

Authority validation stays in service layer.

## 🧱 PHASE 4 — Implement Scope Enforcement

Inside service:

Step order:

1.) Resolve department
2.) Validate role scope
3.) Expand policies from roles
4.) Merge policies
5.) Validate policy scope
6.) Validate at least one policy
7.) Create user (atomic transaction)
8.) Bulk insert UserPolicy
9.) Bulk insert UserRole (optional)

Everything inside transaction.

## 🧱 PHASE 5 — Optimize AuthorizationService

Since we are flattened:

AuthorizationService should:

- Query only UserPolicy
- Cache policy codes per request
- No role joins

We will refactor this after user creation works.

## 🧱 PHASE 6 — Menu Resolver Endpoint

After that, we build:

    GET /me/policies/
    GET /me/systems/
    GET /me/menus/

Based purely on user policies.

🔥 Implementation Order

We will implement in this order:

1️⃣ policy_expander
2️⃣ user_scope_validator
3️⃣ user_creation_service
4️⃣ serializer refactor
5️⃣ view refactor
6️⃣ authorization optimization

That prevents circular mistakes.

⚠️ Important Rule

We will NOT:

- Put permission logic inside serializer
- Check role names directly
- Use is_staff for authority
- Query inside loops
- Skip transaction safety