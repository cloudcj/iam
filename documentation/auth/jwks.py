import time
import requests
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


JWKS_URL = settings.IAM_JWKS_URL
JWKS_CACHE_TTL = settings.IAM_JWKS_CACHE_TTL


_jwks_cache = {
    "keys": {},
    "expires_at": 0,
}


def _fetch_jwks():
    try:
        resp = requests.get(JWKS_URL, timeout=3)
        resp.raise_for_status()
    except requests.RequestException as exc:
        # If we already have keys, keep using them
        if _jwks_cache["keys"]:
            return
        raise AuthenticationFailed("Unable to fetch JWKS") from exc

    keys = {}
    for jwk in resp.json().get("keys", []):
        kid = jwk.get("kid")
        if not kid:
            continue
        keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(jwk)

    if not keys:
        raise AuthenticationFailed("JWKS contains no usable keys")

    _jwks_cache["keys"] = keys
    _jwks_cache["expires_at"] = time.time() + JWKS_CACHE_TTL


def get_public_key(kid: str):
    now = time.time()

    # Refresh cache if expired
    if now >= _jwks_cache["expires_at"]:
        _fetch_jwks()

    key = _jwks_cache["keys"].get(kid)
    if key:
        return key

    # Possible key rotation → refetch once
    _fetch_jwks()
    key = _jwks_cache["keys"].get(kid)

    if not key:
        raise AuthenticationFailed(f"Unknown signing key (kid={kid})")

    return key

