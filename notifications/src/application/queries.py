from dataclasses import dataclass

from application.dto import NotificationDTO
from application.interfaces import NotificationReader


@dataclass(frozen=True)
class GetNotificationsQuery:
    user_id: int


@dataclass
class GetNotificationsHandler:
    _notification_reader: NotificationReader

    async def execute(self, query: GetNotificationsQuery) -> list[NotificationDTO]:
        return await self._notification_reader.get_by_user(query.user_id)
