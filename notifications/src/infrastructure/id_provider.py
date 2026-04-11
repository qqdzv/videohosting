from application.exceptions import AuthenticationError
from application.interfaces import IdProvider, JwtService


class TokenIdProvider(IdProvider):
    def __init__(
        self,
        jwt_service: JwtService,
        token: str,
    ):
        self._jwt_service = jwt_service
        self.token = token

    def get_current_user_id(self) -> int:
        user_id = self._jwt_service.decode(self.token)
        if user_id is None:
            raise AuthenticationError
        return int(user_id)
