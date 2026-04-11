from dataclasses import dataclass
from datetime import datetime


@dataclass
class NotificationDTO:
    user_id: int
    type: str
    message: str
    data: dict | None = None
    id: int | None = None
    is_read: bool = False
    created_at: datetime | None = None
