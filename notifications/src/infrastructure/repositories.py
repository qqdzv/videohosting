from dataclasses import asdict

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from application.dto import NotificationDTO
from application.events import NotificationCreatedEvent, NotificationReadEvent
from application.interfaces import NotificationReader, NotificationWriter
from infrastructure.models import NotificationEventModel


class SqlNotificationReader(NotificationReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_user(self, user_id: int) -> list[NotificationDTO]:
        stmt = (
            select(NotificationEventModel)
            .where(NotificationEventModel.user_id == user_id)
            .order_by(NotificationEventModel.created_at.asc())
        )
        result = await self._session.execute(stmt)
        events = result.scalars().all()

        notifications = self._rebuild_state(events)

        return sorted(notifications, key=lambda n: n.created_at, reverse=True)

    async def get_by_id(self, notification_id: int) -> NotificationDTO | None:
        stmt = (
            select(NotificationEventModel)
            .where(NotificationEventModel.notification_id == notification_id)
            .order_by(NotificationEventModel.created_at.asc())
        )
        result = await self._session.execute(stmt)
        events = result.scalars().all()

        if not events:
            return None

        notifications = self._rebuild_state(events)
        return notifications[0] if notifications else None

    @staticmethod
    def _rebuild_state(events: list[NotificationEventModel]) -> list[NotificationDTO]:
        notifications: dict[int, NotificationDTO] = {}

        for event in events:
            if event.event_type == "NotificationCreatedEvent":
                payload = event.payload
                notifications[event.notification_id] = NotificationDTO(
                    id=event.notification_id,
                    user_id=payload["user_id"],
                    type=payload["type"],
                    message=payload["message"],
                    data=payload.get("data"),
                    is_read=False,
                    created_at=event.created_at,
                )
            elif event.event_type == "NotificationReadEvent":
                if event.notification_id in notifications:
                    notifications[event.notification_id].is_read = True

        return list(notifications.values())


class SqlNotificationWriter(NotificationWriter):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, notification: NotificationDTO) -> NotificationDTO:
        notification_id = await self._next_notification_id()

        event = NotificationCreatedEvent(
            notification_id=notification_id,
            user_id=notification.user_id,
            type=notification.type,
            message=notification.message,
            data=notification.data,
        )
        model = NotificationEventModel(
            notification_id=notification_id,
            user_id=notification.user_id,
            event_type="NotificationCreatedEvent",
            payload=asdict(event),
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)

        notification.id = notification_id
        notification.created_at = model.created_at
        return notification

    async def mark_as_read(self, notification_id: int, user_id: int) -> None:
        event = NotificationReadEvent(notification_id=notification_id)
        model = NotificationEventModel(
            notification_id=notification_id,
            user_id=user_id,
            event_type="NotificationReadEvent",
            payload=asdict(event),
        )
        self._session.add(model)
        await self._session.commit()

    async def _next_notification_id(self) -> int:
        stmt = select(func.coalesce(func.max(NotificationEventModel.notification_id), 0))
        result = await self._session.execute(stmt)
        return result.scalar() + 1
