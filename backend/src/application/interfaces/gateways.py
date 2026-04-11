from typing import Any, Protocol

from application.events import DomainEvent


class PasswordHasher(Protocol):
    def hash(self, password: str) -> str:
        ...

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        ...


class JwtService(Protocol):
    def create_token(self, payload: dict[str, Any]) -> str:
        ...

    def decode_token(self, token: str) -> dict[str, Any]:
        ...


class CacheService(Protocol):
    async def get(self, key: str) -> Any | None:
        ...

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        ...

    async def delete(self, key: str) -> None:
        ...

    async def exists(self, key: str) -> bool:
        ...


class EventPublisher(Protocol):
    async def publish(self, event: DomainEvent) -> None:
        ...


class StorageService(Protocol):
    async def upload(
        self,
        file_content: bytes,
        file_path: str,
        content_type: str | None = None,
    ) -> str:
        ...

    async def delete(self, file_path: str) -> None:
        ...

    async def get_url(self, file_path: str) -> str:
        ...

    async def generate_presigned_upload_url(
        self,
        key: str,
        content_type: str,
        expires_in: int = 300,
    ) -> str:
        ...
