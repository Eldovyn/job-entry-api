from .token import Token
from itsdangerous.url_safe import URLSafeSerializer
from ..config import salt_is_submit, secret_key_is_submit


class IsSubmitToken(Token):
    @staticmethod
    async def insert(user_id, created_at):
        s = URLSafeSerializer(salt_is_submit, salt=secret_key_is_submit)
        token = s.dumps({"user_id": user_id, "created_at": created_at})
        return token

    @staticmethod
    async def get(token):
        s = URLSafeSerializer(salt_is_submit, salt=secret_key_is_submit)
        try:
            s.loads(token)["user_id"]
            s.loads(token)["created_at"]
        except:
            return None
        else:
            return s.loads(token)
