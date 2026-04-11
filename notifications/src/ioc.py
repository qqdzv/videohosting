from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.commands import (
    HandleCommentCreatedHandler,
    HandleSubscriptionCreatedHandler,
    HandleUserCreatedHandler,
    HandleUserLoginedHandler,
    HandleVideoPublishedHandler,
    MarkNotificationReadHandler,
)
from application.interfaces import CacheService, EmailService, JwtService, NotificationReader, NotificationWriter, WebSocketService
from application.queries import GetNotificationsHandler
from config import settings
from infrastructure.gateways import AiosmtplibEmailService, PyJWTService, RedisCacheService, WebSocketManager
from infrastructure.repositories import SqlNotificationReader, SqlNotificationWriter
from infrastructure.resources.database import new_db_session_maker


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_session_maker(self) -> async_sessionmaker[AsyncSession]:
        return new_db_session_maker(settings.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_notification_reader(self, session: AsyncSession) -> NotificationReader:
        return SqlNotificationReader(session)

    @provide(scope=Scope.REQUEST)
    def get_notification_writer(self, session: AsyncSession) -> NotificationWriter:
        return SqlNotificationWriter(session)


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def get_cache_service(self) -> CacheService:
        return RedisCacheService(settings.redis.url)

    @provide(scope=Scope.APP)
    def get_ws_manager(self) -> WebSocketService:
        return WebSocketManager()

    @provide(scope=Scope.APP)
    def get_jwt_service(self) -> JwtService:
        return PyJWTService(
            private_key=settings.jwt.private_key,
            public_key=settings.jwt.public_key,
            algorithm=settings.jwt.algorithm,
        )

    @provide(scope=Scope.REQUEST)
    def get_email_service(self) -> EmailService:
        return AiosmtplibEmailService(
            host=settings.email.smtp_host,
            port=settings.email.smtp_port,
            username=settings.email.sender_email,
            password=settings.email.sender_password,
        )


class ApplicationProvider(Provider):
    # Command handlers
    handle_user_created = provide(HandleUserCreatedHandler, scope=Scope.REQUEST)
    handle_user_logined = provide(HandleUserLoginedHandler, scope=Scope.REQUEST)
    handle_comment_created = provide(HandleCommentCreatedHandler, scope=Scope.REQUEST)
    handle_subscription_created = provide(HandleSubscriptionCreatedHandler, scope=Scope.REQUEST)
    handle_video_published = provide(HandleVideoPublishedHandler, scope=Scope.REQUEST)
    mark_notification_read = provide(MarkNotificationReadHandler, scope=Scope.REQUEST)

    # Query handlers
    get_notifications = provide(GetNotificationsHandler, scope=Scope.REQUEST)
