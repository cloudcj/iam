## IAM Project Structure

    iam/
    ├── manage.py
    ├── pyproject.toml / requirements.txt
    │
    ├── config/ # Django project config (NOT "iam")
    │ ├── **init**.py
    │ ├── asgi.py
    │ ├── wsgi.py
    │ ├── urls.py
    │ └── settings/
    │ ├── **init**.py
    │ ├── base.py # common settings
    │ ├── dev.py # DEBUG=True
    │ └── prod.py # DEBUG=False
    │
    ├── iam/ # Identity (users only)
    │ ├── **init**.py
    │ ├── admin.py
    │ ├── apps.py
    │ ├── managers.py # UserManager, ActiveUserManager
    │ ├── models.py # User model (UUID, username login)
    │ ├── serializers.py # Login serializer, user DTOs
    │ ├── views.py # Login, logout, profile
    │ ├── urls.py
    │ └── migrations/
    │
    ├── authz/ # Authorization (RBAC)
    │ ├── **init**.py
    │ ├── admin.py
    │ ├── apps.py
    │ ├── models.py # Role, Permission, UserRole
    │ ├── services.py # Role → permission resolution
    │ ├── seeds.py # Initial roles & perms
    │ └── migrations/
    │
    ├── tokens/ # JWT & refresh tokens
    │ ├── **init**.py
    │ ├── apps.py
    │ ├── models.py # RefreshToken
    │ ├── jwt.py # Issue access tokens
    │ ├── authentication.py # JWTAuthentication (DRF)
    │ ├── keys/
    │ │ ├── private.pem # RS256 signing key
    │ │ └── public.pem # Verification key
    │ ├── views.py # refresh, service tokens
    │ └── migrations/
    │
    ├── security/ # Security & audit (optional but recommended)
    │ ├── **init**.py
    │ ├── models.py # LoginAttempt, IP block
    │ └── services.py
    │
    └── common/ # Shared utilities
    ├── **init**.py
    ├── exceptions.py
    ├── responses.py
    └── constants.py

## IAM Settings Structure

    iam/
    ├── iam/
    │ ├── settings.py
    │ ├── urls.py
    │ └── wsgi.py
    ├── iam/ # users & service iam
    ├── authz/ # roles & permissions
    ├── tokens/ # jwt issuing, refresh, keys
    └── manage.py

## IAM Model Structure

    iam/
    ├── **init**.py
    ├── admin.py
    ├── apps.py
    ├── managers.py 👈 UserManager, ActiveUserManager
    ├── models.py 👈 User model
    ├── serializers.py 👈 DRF serializers
    ├── views.py 👈 Login, profile endpoints
    ├── urls.py 👈 IAM routes
    ├── permissions.py 👈 DRF permission classes (optional)
    ├── migrations/
    │ └── **init**.py

---

What Must Be Removed or Moved

What Your JWT MUST Contain (Gaia Contract)

Your token is now a contract between IAM and services.

    ✅ User JWT (example)
    {
    "iss": "gaia-iam",
    "sub": "550e8400-e29b-41d4-a716-446655440000",
    "username": "cj",
    "type": "user",

    "roles": ["Admin"],
    "permissions": [
    "inventory.read",
    "inventory.write",
    "analytics.report.view"
    ],

    "iat": 1700000000,
    "exp": 1700000900
    }

🔒 What services trust

Signature (RS256)

Expiration

Permissions list

Nothing else.

2️⃣ What Dies Immediately from Your Old Model

Let’s be explicit.

❌ REMOVE these forever
groups
is_root
is_admin
is_member
user.has_perm()
exclude(groups\_\_name="Root")

These cannot exist in a JWT-first architecture.
