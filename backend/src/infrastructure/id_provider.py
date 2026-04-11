from application.exceptions import AuthenticationError
from application.interfaces.id_provider import IdProvider
from infrastructure.gateways import PyJWTService


class TokenIdProvider(IdProvider):
    def __init__(
        self,
        jwt_service: PyJWTService,
        token: str,
    ):
        self._jwt_service = jwt_service
        self.token = token

    def get_current_user_id(self) -> int:
        payload = self._jwt_service.decode_token(self.token)
        user_id = payload.get("id")
        if user_id is None:
            raise AuthenticationError
        return int(user_id)
