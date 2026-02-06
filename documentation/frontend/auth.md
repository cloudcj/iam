# IAM / Authentication Service

This service is responsible for **authentication, authorization, and identity management** for the system.

It acts as a **central IAM (Identity & Access Management) service** used by other backend services.

---

## Responsibilities

- User authentication (login, logout, token refresh)
- JWT issuance and validation
- CSRF protection for cookie-based auth
- Identity resolution (`/api/me`)
- User lifecycle management (create, update, roles, departments)
- Role and permission assignment (via Identity domain)

---

## Base URLs

| Domain       | Base Path        | Description                |
| ------------ | ---------------- | -------------------------- |
| Auth         | `/api/auth/`     | Authentication & tokens    |
| Identity     | `/api/identity/` | User & role management     |
| Current User | `/api/me/`       | Authenticated user context |

---

## Authentication Flow (High Level)

1. Client requests CSRF token
2. Client logs in with credentials
3. IAM issues **Access + Refresh JWT**
4. Tokens are stored securely (cookies)
5. Client calls protected APIs
6. Access token expires → refresh endpoint used
7. Logout clears authentication state

---

## Auth Endpoints

### 1️⃣ Get CSRF Token

#### GET /api/auth/csrf/

Used before login when using cookie-based authentication.

    **Response**
    ```json
    {
    "csrfToken": "abc123..."
    }

### 2️⃣ Login

    POST /api/auth/login/

Authenticates a user and issues JWT tokens.

Request

    {
        "username": "user@example.com",
        "password": "password"
    }

### 3️⃣ Refresh Token

    POST /api/auth/refresh/

Issues a new access token using a valid refresh token.

Used when

- Access token is expired
- User session is still valid

### 4️⃣ Logout

    POST /api/auth/logout/

Logs out the user by invalidating authentication state.

Behavior

- Clears auth cookies
- Ends session

5️⃣ Protected Test Endpoint

    GET /api/auth/test/protected/

Test endpoint to verify authentication middleware.

Response

- 200 OK → authenticated
- 401 Unauthorized → not authenticated
