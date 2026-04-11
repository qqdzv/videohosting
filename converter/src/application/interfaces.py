from typing import Any, Protocol

from application.events import DomainEvent


class MessageBroker(Protocol):
    async def publish(self, message: dict[str, Any], topic: str) -> None: ...


class EventPublisher(Protocol):
    async def publish(self, event: DomainEvent) -> None: ...


class StorageService(Protocol):
    async def upload(
        self,
        file_content: bytes,
        file_path: str,
        content_type: str | None = None,
    ) -> str: ...

    async def upload_file(
        self,
        local_path: str,
        s3_path: str,
        content_type: str | None = None,
    ) -> str: ...

    async def download_bytes(self, s3_path: str) -> bytes: ...

    async def download_file(self, s3_path: str, dest_path: str) -> None: ...

    async def delete(self, file_path: str) -> None: ...

    async def get_url(self, file_path: str) -> str: ...
