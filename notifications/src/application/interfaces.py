from abc import ABC, abstractmethod
from typing import Any, Protocol

from application.dto import NotificationDTO


class CacheService(Protocol):
    async def get(self, key: str) -> Any | None: ...
    async def delete(self, key: str) -> None: ...


class EmailService(Protocol):
    async def send(self, to: str, subject: str, body: str) -> None: ...


class WebSocketService(Protocol):
    async def connect(self, websocket: Any, user_id: int) -> None: ...
    async def send(self, user_id: int, message: str) -> None: ...


class JwtService(Protocol):
    def decode(self, token: str) -> int | None: ...


class NotificationReader(ABC):
    @abstractmethod
    async def get_by_user(self, user_id: int) -> list[NotificationDTO]: ...

    @abstractmethod
    async def get_by_id(self, notification_id: int) -> NotificationDTO | None: ...


class NotificationWriter(ABC):
    @abstractmethod
    async def create(self, notification: NotificationDTO) -> NotificationDTO: ...

    @abstractmethod
    async def mark_as_read(self, notification_id: int, user_id: int) -> None: ...


class IdProvider(Protocol):
    def get_current_user_id(self) -> int:
        ...
