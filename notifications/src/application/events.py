from dataclasses import dataclass


@dataclass(frozen=True)
class NotificationCreatedEvent:
    notification_id: int
    user_id: int
    type: str
    message: str
    data: dict | None = None


@dataclass(frozen=True)
class NotificationReadEvent:
    notification_id: int
