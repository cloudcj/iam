# # identity/auth/tokens/cookies.py

# def set_auth_cookies(response, *, access, refresh):
#     response.set_cookie(
#         "access_token",
#         access,
#         httponly=True,
#         secure=True,
#         samesite="Lax",
#     )

#     response.set_cookie(
#         "refresh_token",
#         refresh,
#         httponly=True,
#         secure=True,
#         samesite="Lax",
#     )


# def clear_auth_cookies(response):
#     response.delete_cookie("access_token")
#     response.delete_cookie("refresh_token")


# identity/auth/tokens/cookies.py
from django.conf import settings

ACCESS_COOKIE_NAME = "access_token"
REFRESH_COOKIE_NAME = "refresh_token"

ACCESS_TTL = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
REFRESH_TTL = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())

def set_auth_cookies(response, *, access, refresh):
    response.set_cookie(
        ACCESS_COOKIE_NAME,
        access,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="Lax",
        max_age=ACCESS_TTL,
        path="/",
    )

    response.set_cookie(
        REFRESH_COOKIE_NAME,
        refresh,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="Lax",
        max_age=REFRESH_TTL,
        path="/",
    )


def clear_auth_cookies(response):
    response.delete_cookie(ACCESS_COOKIE_NAME, path="/")
    response.delete_cookie(REFRESH_COOKIE_NAME, path="/")
