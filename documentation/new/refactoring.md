The refactor order (do NOT skip around)
🥇 Phase 1 — Settings (trust & behavior)

This defines who issues tokens, how they’re sent, and how they’re verified.

We do this first because:

Everything else depends on it

It prevents contradictory auth logic later

Files

settings.py ✅ (first)

urls.py (token endpoints)

🥈 Phase 2 — Authentication boundary

This is where cookies vs headers are unified.

Files

apps/authn/authentication.py

(Your IAMAuthentication)

Goal:

Accept cookie and header

Output a standard request.user + request.auth

🥉 Phase 3 — Token issuance

Now that settings + auth boundary are clean.

Files

apps/authn/tokens.py

apps/authn/views/login.py

apps/authn/views/refresh.py

Goal:

SimpleJWT only

Custom claims

Cookies set correctly

🏅 Phase 4 — User context endpoints

These depend on everything above being stable.

Files

/me

permissions

role enforcement

🏁 Phase 5 — Service-to-service flow

Last, because it depends on claim contract.

Artifacts

JWT contract doc

PyJWT verification snippet

Gateway / forwarding logic

What “starting in settings” means concretely

For your current step, we lock these decisions:

✅ SimpleJWT is the only issuer

✅ RS256 keys live in IAM

✅ Cookies are allowed transport

✅ Headers are allowed transport

❌ No PyJWT in IAM

❌ No duplicated JWT configs

You already started this — good instinct.

Minimal checklist for this step

Before touching any other file, your settings.py must:

 Have rest_framework_simplejwt enabled

 Use RS256 in SIMPLE_JWT

 Have issuer & audience defined

 Not define parallel JWT_* settings

 Keep IAMAuthentication as default auth

Once this is true, everything else becomes straightforward.

Answer to your question (explicit)

Should we start refactoring in settings?

✔ Yes
✔ That’s the correct and safest starting point
✔ You’re already doing it right

Next move (pick one)

Say one of these and we proceed immediately:

“finish settings” → we finalize cookie-related flags

“authentication class” → we refactor IAMAuthentication

“token issuance” → we clean login & refresh views

We’ll keep this methodical and boring — which is exactly how secure auth gets built 😄