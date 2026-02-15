from rest_framework_simplejwt.tokens import RefreshToken


def issue_user_tokens(*, user):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    # Identity only
    access["username"] = user.username
    # SimpleJWT already sets:
    # - sub (user id)
    # - exp
    # - iat
    # - jti
    # - token_type

    return {
        "access": str(access),
        "refresh": str(refresh),
    }







# identity/auth/tokens/service.py
# from rest_framework_simplejwt.tokens import RefreshToken
# from uuid import uuid4
# from .tokens import GaiaAccessToken

# ACTIVE_KID = "key-01"



# def issue_user_tokens(*, user, permissions):
#     # 1️⃣ Refresh token (SimpleJWT, HS256)
#     refresh = RefreshToken.for_user(user)

#     # 2️⃣ Access token (IAM, RS256 + kid)
#     access = encode_access_token(
#         user=user,
#         permissions=permissions,
#     )

#     return {
#         "access": access,          # RS256 (IAM)
#         "refresh": str(refresh),   # HS256 (SimpleJWT)
#     }






# def issue_user_tokens(*, user, permissions):
#     refresh = RefreshToken.for_user(user)
#        # 👇 use custom access token
#     # access = GaiaAccessToken.for_user(user)
#     access = refresh.access_token

#     # ------------------
#     # Identity
#     # ------------------
#     subject = f"user:{user.id}"
#     access["sub"] = subject
#     refresh["sub"] = subject

#     access["username"] = user.username
#     refresh["username"] = user.username

#     # ------------------
#     # Authorization
#     # ------------------
#     access["permissions"] = permissions
#     refresh["permissions"] = permissions

#     # 🔑 FORCE uniqueness per login (BEST PRACTICE)
#     access["jti"] = uuid4().hex


#     # ------------------
#     # # Key identification (JWKS / rotation)
#     # # ------------------
#     # access.headers["kid"] = ACTIVE_KID
#     # refresh.headers["kid"] = ACTIVE_KID

#     return {
#         "access": str(access),
#         "refresh": str(refresh),
#     }





# def issue_service_token(*, service_name, permissions):
#     token = AccessToken()

#     token["sub"] = f"service:{service_name}"
#     token["svc"] = service_name
#     token["permissions"] = permissions

#     token["iss"] = ISSUER
#     token["aud"] = AUDIENCE

#     return str(token)




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
