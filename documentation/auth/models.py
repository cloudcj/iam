class JWTUser:
    """
    Lightweight authenticated user from JWT.
    """

    is_authenticated = True

    def __init__(self, *, user_id: str, username: str | None = None):
        self.id = user_id
        self.username = username
