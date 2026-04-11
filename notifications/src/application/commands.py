import asyncio
import json
from dataclasses import asdict, dataclass

from application.dto import NotificationDTO
from application.exceptions import NotificationNotFoundError, NotificationPermissionError
from application.interfaces import EmailService, NotificationReader, NotificationWriter, WebSocketService
from infrastructure.resources.logging import get_logger

logger = get_logger(__name__)


def _ws_message(event: str, data: dict) -> str:
    return json.dumps({"event": event, "data": data})


@dataclass(frozen=True)
class HandleUserCreatedCommand:
    user_id: int
    email: str
    username: str


@dataclass
class HandleUserCreatedHandler:
    _email_service: EmailService
    _ws_service: WebSocketService
    _notification_writer: NotificationWriter

    async def execute(self, command: HandleUserCreatedCommand) -> None:
        message = f"Дорогой пользователь {command.username}, спасибо что зарегистрировались на нашей платформе."
        await self._notification_writer.create(
            NotificationDTO(user_id=command.user_id, type="user_created", message=message, data=asdict(command)),
        )
        results = await asyncio.gather(
            self._email_service.send(
                to=command.email,
                subject="Спасибо за регистрацию!",
                body=message,
            ),
            self._ws_service.send(
                user_id=command.user_id,
                message=_ws_message("user_created", {"message": message}),
            ),
            return_exceptions=True,
        )
        for result in results:
            if isinstance(result, Exception):
                logger.error("Notification delivery failed", error=str(result))


@dataclass(frozen=True)
class HandleUserLoginedCommand:
    user_id: int
    email: str
    username: str


@dataclass
class HandleUserLoginedHandler:
    _email_service: EmailService
    _ws_service: WebSocketService
    _notification_writer: NotificationWriter

    async def execute(self, command: HandleUserLoginedCommand) -> None:
        message = f"Дорогой пользователь {command.username}, только что вы авторизировались на нашем сайте."
        await self._notification_writer.create(
            NotificationDTO(user_id=command.user_id, type="user_logined", message=message, data=asdict(command)),
        )
        results = await asyncio.gather(
            self._email_service.send(
                to=command.email,
                subject="Новый вход в аккаунт",
                body=(
                    f"Дорогой пользователь {command.username}, только что вы авторизировались. "
                    "Если это были не вы, напишите в поддержку."
                ),
            ),
            self._ws_service.send(
                user_id=command.user_id,
                message=_ws_message("user_logined", {"message": message}),
            ),
            return_exceptions=True,
        )
        for result in results:
            if isinstance(result, Exception):
                logger.error("Notification delivery failed", error=str(result))


@dataclass(frozen=True)
class HandleCommentCreatedCommand:
    user_id: int
    email: str
    username: str
    comment: str
    sender: str


@dataclass
class HandleCommentCreatedHandler:
    _email_service: EmailService
    _ws_service: WebSocketService
    _notification_writer: NotificationWriter

    async def execute(self, command: HandleCommentCreatedCommand) -> None:
        message = f"Пользователь {command.sender} прокомментировал ваше видео: {command.comment}"
        await self._notification_writer.create(
            NotificationDTO(user_id=command.user_id, type="comment_created", message=message, data=asdict(command)),
        )
        results = await asyncio.gather(
            self._email_service.send(
                to=command.email,
                subject="Ваше видео прокомментировали!",
                body=f"Дорогой пользователь {command.username}, пользователь {command.sender} написал: {command.comment}.",
            ),
            self._ws_service.send(
                user_id=command.user_id,
                message=_ws_message("comment_created", {"message": message}),
            ),
            return_exceptions=True,
        )
        for result in results:
            if isinstance(result, Exception):
                logger.error("Notification delivery failed", error=str(result))


@dataclass(frozen=True)
class HandleSubscriptionCreatedCommand:
    user_id: int
    email: str
    username: str
    follower: str


@dataclass
class HandleSubscriptionCreatedHandler:
    _email_service: EmailService
    _ws_service: WebSocketService
    _notification_writer: NotificationWriter

    async def execute(self, command: HandleSubscriptionCreatedCommand) -> None:
        message = f"Пользователь {command.follower} подписался на ваш канал."
        await self._notification_writer.create(
            NotificationDTO(user_id=command.user_id, type="subscription_created", message=message, data=asdict(command)),
        )
        results = await asyncio.gather(
            self._email_service.send(
                to=command.email,
                subject="На вас подписались!",
                body=f"Дорогой пользователь {command.username}, на вас подписался пользователь {command.follower}.",
            ),
            self._ws_service.send(
                user_id=command.user_id,
                message=_ws_message("subscription_created", {"message": message}),
            ),
            return_exceptions=True,
        )
        for result in results:
            if isinstance(result, Exception):
                logger.error("Notification delivery failed", error=str(result))


@dataclass(frozen=True)
class HandleVideoPublishedCommand:
    user_id: int
    email: str
    username: str
    title: str
    author: str


@dataclass
class HandleVideoPublishedHandler:
    _email_service: EmailService
    _ws_service: WebSocketService
    _notification_writer: NotificationWriter

    async def execute(self, command: HandleVideoPublishedCommand) -> None:
        message = f"У {command.author} вышло новое видео: {command.title}"
        await self._notification_writer.create(
            NotificationDTO(user_id=command.user_id, type="video_published", message=message, data=asdict(command)),
        )
        results = await asyncio.gather(
            self._email_service.send(
                to=command.email,
                subject="Новое видео!",
                body=f"Дорогой пользователь. {message}",
            ),
            self._ws_service.send(
                user_id=command.user_id,
                message=_ws_message("video_published", {"message": message}),
            ),
            return_exceptions=True,
        )
        for result in results:
            if isinstance(result, Exception):
                logger.error("Notification delivery failed", error=str(result))


@dataclass(frozen=True)
class MarkNotificationReadCommand:
    notification_id: int
    user_id: int


@dataclass
class MarkNotificationReadHandler:
    _notification_writer: NotificationWriter
    _notification_reader: NotificationReader

    async def execute(self, command: MarkNotificationReadCommand) -> None:
        notification = await self._notification_reader.get_by_id(command.notification_id)
        if not notification:
            raise NotificationNotFoundError
        if notification.user_id != command.user_id:
            raise NotificationPermissionError
        await self._notification_writer.mark_as_read(
            command.notification_id,
            command.user_id,
        )
