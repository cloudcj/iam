from datetime import datetime, timezone
from django.core.cache import cache

BLACKLIST_PREFIX = "iam:blacklist:"


def blacklist_token(jti: str, exp: int) -> None:
    """
    Store JTI in Redis until the token naturally expires.
    exp: Unix timestamp from JWT 'exp' claim.
    """
    ttl = int(exp - datetime.now(timezone.utc).timestamp())
    if ttl > 0:
        cache.set(f"{BLACKLIST_PREFIX}{jti}", "1", timeout=ttl)


def is_blacklisted(jti: str) -> bool:
    return cache.get(f"{BLACKLIST_PREFIX}{jti}") is not None
