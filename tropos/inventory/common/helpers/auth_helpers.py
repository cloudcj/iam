# from typing import Union
# from django.core.cache import cache
# from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
# from accounts.models import AuthLog

# def blacklist_token(token: Union[AccessToken, RefreshToken], prefix: str = "blacklist") -> str:
#     """
#     Blacklist a given JWT (access or refresh) by storing its JTI in Redis.

#     The token's JTI (unique identifier) is used as the key, and the value 
#     is set to "blacklisted". The key automatically expires from Redis 
#     after the token's own TTL (time-to-live), ensuring no stale entries 
#     remain after the token naturally expires.

#     Args:
#         token (Union[AccessToken, RefreshToken]): The token object to blacklist.
#         prefix (str, optional): Key prefix for Redis storage. Defaults to "blacklist".

#     Returns:
#         str: The JTI of the blacklisted token.
#     """
#     jti = str(token['jti'])
#     exp = token['exp']
#     ttl = int (exp - token.current_time.timestamp())
#     cache.set(f"{prefix}:{jti}", "blacklisted", timeout=ttl)
#     return jti

# def is_token_blacklisted(token_str: Union[AccessToken, RefreshToken]) -> bool:
#     """
#     Check if a given JWT (usually refresh or access) is blacklisted in Redis.

#     Args:
#         token_str (str): The raw JWT string.
    
#     Returns:
#         bool: True if blacklisted, False otherwise.
#     """
#     jti = str(token_str['jti'])
#     return cache.get(f"blacklist:{jti}") is not None

# def get_client_ip(request):
#     """
#     Helper function for effectively fetching client ip even in production.
#     """
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         return x_forwarded_for.split(',')[0]
#     return request.META.get('REMOTE_ADDR')

# def log_auth_event(request, user, action, username=None):
#     """
#     Centralized helper to log authentication events.
#     """
#     AuthLog.objects.create(
#         user=user if user and user.is_authenticated else Ninventory.common.helpers.auth_helpersone,
#         username=username or (user.username if user else "anonymous"),
#         action=AuthLog.ACTION_CHOICES[action],
#         ip_address=get_client_ip(request),
#         user_agent=request.META.get("HTTP_USER_AGENT"),
#     )