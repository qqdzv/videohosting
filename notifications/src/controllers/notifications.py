from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, status

from application.commands import MarkNotificationReadCommand, MarkNotificationReadHandler
from application.interfaces import IdProvider
from application.queries import GetNotificationsHandler, GetNotificationsQuery
from controllers.dependencies import get_id_provider
from controllers.schemas import NotificationResponse, NotificationsListResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("")
@inject
async def get_notifications(
    handler: FromDishka[GetNotificationsHandler],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> NotificationsListResponse:
    user_id = id_provider.get_current_user_id()
    notifications = await handler.execute(
        GetNotificationsQuery(user_id=user_id),
    )
    data = [
        NotificationResponse(
            id=n.id,  # type: ignore[arg-type]
            user_id=n.user_id,
            type=n.type,
            message=n.message,
            is_read=n.is_read,
            created_at=n.created_at,  # type: ignore[invalid-argument-type]
        )
        for n in notifications
    ]
    return NotificationsListResponse(
        unread=sum(1 for n in notifications if not n.is_read),
        data=data,
    )


@router.patch("/{notification_id}/read", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def mark_as_read(
    notification_id: int,
    handler: FromDishka[MarkNotificationReadHandler],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> None:
    user_id = id_provider.get_current_user_id()
    await handler.execute(
        MarkNotificationReadCommand(
            notification_id=notification_id,
            user_id=user_id,
        ),
    )
