from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Cookie

from application.interfaces import IdProvider, JwtService
from infrastructure.id_provider import TokenIdProvider


@inject
def get_id_provider(
    jwt_service: FromDishka[JwtService],
    access_token: Annotated[str | None, Cookie()] = None,
) -> IdProvider:
    return TokenIdProvider(jwt_service=jwt_service, token=access_token or "")
