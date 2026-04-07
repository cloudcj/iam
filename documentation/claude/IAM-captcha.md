# IAM reCAPTCHA v2 Integration

## Overview

reCAPTCHA v2 ("I'm not a robot" checkbox) is added to the login flow to block automated login attempts. The token is generated on the frontend, sent with the login request, and verified against Google's API on the backend before credentials are checked.

**Both v2 and v3 are free with no usage limits.** v1 was shut down by Google in 2018.

---

## Files Changed

### Backend

| File | Change |
|------|--------|
| `.env.example` | Added `RECAPTCHA_SECRET_KEY` variable |
| `.env` | Added actual secret key value |
| `config/settings/base.py` | Added `RECAPTCHA_SECRET_KEY = env("RECAPTCHA_SECRET_KEY")` |
| `apps/authn/recaptcha.py` | **New file** — verification utility |
| `apps/authn/views/login.py` | Added reCAPTCHA validation before login logic |

### Frontend

| File | Change |
|------|--------|
| `z-frontend/final-iam-ui/.env` | Added `VITE_RECAPTCHA_SITE_KEY` variable |
| `z-frontend/final-iam-ui/package.json` | Added `react-google-recaptcha` + `@types/react-google-recaptcha` |
| `src/types/index.ts` | Added `recaptcha_token: string` to `LoginRequest` interface |
| `src/pages/LoginPage.tsx` | Added `ReCAPTCHA` widget, ref, and token submission |

---

## Backend Implementation

### Environment

```env
# .env / .env.example
RECAPTCHA_SECRET_KEY=your_secret_key_here
```

### Settings

```python
# config/settings/base.py
RECAPTCHA_SECRET_KEY = env("RECAPTCHA_SECRET_KEY")
```

### Verification Utility

```python
# apps/authn/recaptcha.py
import requests
from django.conf import settings


def verify_recaptcha(token: str) -> bool:
    if not token:
        return False
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": settings.RECAPTCHA_SECRET_KEY,
            "response": token,
        },
        timeout=5,
    )
    return response.json().get("success", False)
```

### Login View

```python
# apps/authn/views/login.py — inside post()
from apps.authn.recaptcha import verify_recaptcha

# Add before the login() call:
recaptcha_token = request.data.get("recaptcha_token", "")
if not verify_recaptcha(recaptcha_token):
    return Response(
        {"detail": "reCAPTCHA verification failed. Please try again."},
        status=status.HTTP_400_BAD_REQUEST,
    )
```

---

## Frontend Implementation

### Install

```bash
# run inside z-frontend/final-iam-ui/
npm install react-google-recaptcha
npm install -D @types/react-google-recaptcha
```

### Environment

```env
# z-frontend/final-iam-ui/.env
VITE_RECAPTCHA_SITE_KEY=your_site_key_here
```

### Type Update

```ts
// src/types/index.ts
export interface LoginRequest {
  username: string
  password: string
  recaptcha_token: string
}
```

### LoginPage Usage

```tsx
import { useRef } from 'react'
import ReCAPTCHA from 'react-google-recaptcha'

const recaptchaRef = useRef<ReCAPTCHA>(null)

// Inside handleSubmit:
const recaptcha_token = recaptchaRef.current?.getValue() ?? ''
if (!recaptcha_token) {
  setError('Please complete the reCAPTCHA.')
  return
}

// Pass token with credentials:
await login({ ...values, recaptcha_token }).unwrap()

// Reset after submit (success or failure):
recaptchaRef.current?.reset()

// In JSX, place above the submit button:
<ReCAPTCHA
  ref={recaptchaRef}
  sitekey={import.meta.env.VITE_RECAPTCHA_SITE_KEY}
/>
```

---

## Request Flow

```
User fills form
  → checks reCAPTCHA box
  → Google sets token in widget

Frontend POST /api/v1/auth/login/
  body: { username, password, recaptcha_token }

Backend LoginView.post()
  1. verify_recaptcha(token) → POST to google.com/recaptcha/api/siteverify
     - fail → 400 "reCAPTCHA verification failed"
     - pass → continue
  2. Account lockout check (5 attempts / 15 min)
  3. authenticate(username, password)
  4. Issue JWT tokens → set HttpOnly cookies
  5. Return { detail, must_change_password }
```

---

## Key Registration

Register keys at: https://www.google.com/recaptcha/admin

- Type: **reCAPTCHA v2 — "I'm not a robot" Checkbox**
- Domains: `localhost`, `127.0.0.1` (add your production domain when deploying)
- **Site Key** → frontend (`VITE_RECAPTCHA_SITE_KEY`)
- **Secret Key** → backend (`RECAPTCHA_SECRET_KEY`)

---

## Why v2 over v3

| | v2 | v3 |
|---|---|---|
| UX | Checkbox / image challenge | Invisible |
| Backend logic | `success: true/false` | Score threshold (0.0–1.0) |
| Complexity | Low | Medium |

Start with v2. When traffic grows, add v3 as an invisible first pass — v2 becomes the challenge fallback for suspicious scores. Both use the same `siteverify` endpoint and the same key pair, so migration is straightforward.
