# identity/auth/tokens/service.py
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

ISSUER = "gaia-iam"
AUDIENCE = "gaia-api"


def issue_user_tokens(*, user, permissions):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    # ------------------
    # Identity
    # ------------------
    subject = f"user:{user.id}"

    access["sub"] = subject
    refresh["sub"] = subject

    access["username"] = user.username
    refresh["username"] = user.username

    # ------------------
    # Authorization
    # ------------------
    access["permissions"] = permissions
    refresh["permissions"] = permissions

    # ------------------
    # Trust
    # ------------------
    access["iss"] = ISSUER
    refresh["iss"] = ISSUER

    access["aud"] = AUDIENCE
    # ❌ no aud on refresh token

    return {
        "access": str(access),
        "refresh": str(refresh),
    }




def issue_service_token(*, service_name, permissions):
    token = AccessToken()

    token["sub"] = f"service:{service_name}"
    token["svc"] = service_name
    token["permissions"] = permissions

    token["iss"] = ISSUER
    token["aud"] = AUDIENCE

    return str(token)




# def issue_tokens(user, *, permissions):
#     refresh = RefreshToken.for_user(user)
#     access = refresh.access_token
    
#     access["permissions"] = permissions
#     access["username"] = user.username

#     return {
#         "access": str(access),
#         "refresh": str(refresh),
#     }


def revoke_tokens(refresh_token):
    refresh_token.blacklist()
