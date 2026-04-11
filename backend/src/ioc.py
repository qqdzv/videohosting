from collections.abc import AsyncIterator

import aioboto3
from dishka import Provider, Scope, provide
from faststream.kafka import KafkaBroker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from types_aiobotocore_s3 import S3Client

from application.interactors.auth import (
    CreateWsTicketInteractor,
    EditUserProfileInteractor,
    GetAvatarPresignedUrlInteractor,
    GetUserProfileInteractor,
    LoginUserInteractor,
    LogoutUserInteractor,
    RegisterUserInteractor,
    UpdateAvatarInteractor,
)
from application.interactors.comments import (
    CreateCommentInteractor,
    DeleteCommentInteractor,
    EditCommentInteractor,
    GetCommentsForVideoInteractor,
)
from application.interactors.likes import (
    GetLikeStatsInteractor,
    SetReactionInteractor,
)
from application.interactors.media import (
    AddViewToVideoInteractor,
    DeleteVideoInteractor,
    EditVideoInteractor,
    GetUserHistoryInteractor,
    GetVideoByIdInteractor,
    GetVideoListInteractor,
    GetVideosByAuthorInteractor,
    MarkVideoConvertFailedInteractor,
    SaveVideoConvertInteractor,
    SearchVideosInteractor,
    UploadVideoInteractor,
)
from application.interactors.subscriptions import (
    CheckSubscriptionStatusInteractor,
    GetAllChannelsInteractor,
    GetMySubscriptionsInteractor,
    SearchUsersInteractor,
    SubscribeToUserInteractor,
    UnsubscribeFromUserInteractor,
)
from application.interfaces.gateways import (
    CacheService,
    EventPublisher,
    JwtService,
    PasswordHasher,
    StorageService,
)
from application.interfaces.repositories import (
    CommentRepository,
    LikeRepository,
    SubscriptionRepository,
    UserRepository,
    VideoRepository,
)
from application.interfaces.unit_of_work import UnitOfWork
from config import settings
from infrastructure.gateways import (
    KafkaEventPublisher,
    PasslibPasswordHasher,
    PyJWTService,
    RedisCacheService,
    S3StorageService,
)
from infrastructure.repositories import (
    SqlCommentRepository,
    SqlLikeRepository,
    SqlSubscriptionRepository,
    SqlUserRepository,
    SqlVideoRepository,
)
from infrastructure.resources.database import new_db_session_maker
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork


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


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_unit_of_work(self, session: AsyncSession) -> UnitOfWork:
        return SqlAlchemyUnitOfWork(session)

    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> UserRepository:
        return SqlUserRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_video_repository(self, session: AsyncSession) -> VideoRepository:
        return SqlVideoRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_comment_repository(self, session: AsyncSession) -> CommentRepository:
        return SqlCommentRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_like_repository(self, session: AsyncSession) -> LikeRepository:
        return SqlLikeRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_subscription_repository(
        self,
        session: AsyncSession,
    ) -> SubscriptionRepository:
        return SqlSubscriptionRepository(session)


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def get_password_hasher(self) -> PasswordHasher:
        return PasslibPasswordHasher()

    @provide(scope=Scope.APP)
    def get_jwt_service(self) -> JwtService:
        return PyJWTService(
            private_key=settings.jwt.private_key,
            public_key=settings.jwt.public_key,
            algorithm=settings.jwt.algorithm,
            token_ttl=settings.jwt.token_ttl_seconds,
        )

    @provide(scope=Scope.APP)
    async def get_cache_service(self) -> CacheService:
        return RedisCacheService(url=settings.redis.url)

    @provide(scope=Scope.APP)
    def get_event_publisher(self, broker: KafkaBroker) -> EventPublisher:
        return KafkaEventPublisher(broker=broker, config=settings.kafka)

    @provide(scope=Scope.APP)
    def get_s3_session(self) -> aioboto3.Session:
        return aioboto3.Session(
            aws_access_key_id=settings.s3.access_key,
            aws_secret_access_key=settings.s3.secret_key,
            region_name=settings.s3.region_name,
        )

    @provide(scope=Scope.REQUEST)
    async def get_s3_client(
        self,
        s3_session: aioboto3.Session,
    ) -> AsyncIterator[S3Client]:
        async with s3_session.client(
            "s3",
            endpoint_url=settings.s3.endpoint_url,
        ) as client:
            yield client

    @provide(scope=Scope.REQUEST)
    def get_storage_service(self, s3_client: S3Client) -> StorageService:
        return S3StorageService(
            s3_client=s3_client,
            bucket=settings.s3.bucket,
            public_url=settings.s3.public_url,
        )


class ApplicationProvider(Provider):
    # Auth Interactors
    register_user_interactor = provide(RegisterUserInteractor, scope=Scope.REQUEST)
    login_user_interactor = provide(LoginUserInteractor, scope=Scope.REQUEST)
    logout_user_interactor = provide(LogoutUserInteractor, scope=Scope.REQUEST)
    edit_user_profile_interactor = provide(EditUserProfileInteractor, scope=Scope.REQUEST)
    get_user_profile_interactor = provide(GetUserProfileInteractor, scope=Scope.REQUEST)
    get_avatar_presigned_url_interactor = provide(GetAvatarPresignedUrlInteractor, scope=Scope.REQUEST)
    update_avatar_interactor = provide(UpdateAvatarInteractor, scope=Scope.REQUEST)
    create_ws_ticket_interactor = provide(CreateWsTicketInteractor, scope=Scope.REQUEST)

    # Comment Interactors
    create_comment_interactor = provide(CreateCommentInteractor, scope=Scope.REQUEST)
    delete_comment_interactor = provide(DeleteCommentInteractor, scope=Scope.REQUEST)
    edit_comment_interactor = provide(EditCommentInteractor, scope=Scope.REQUEST)
    get_comments_for_video_interactor = provide(GetCommentsForVideoInteractor, scope=Scope.REQUEST)

    # Like Interactors
    set_reaction_interactor = provide(SetReactionInteractor, scope=Scope.REQUEST)
    get_like_stats_interactor = provide(GetLikeStatsInteractor, scope=Scope.REQUEST)

    # Subscription Interactors
    subscribe_to_user_interactor = provide(SubscribeToUserInteractor, scope=Scope.REQUEST)
    unsubscribe_from_user_interactor = provide(UnsubscribeFromUserInteractor, scope=Scope.REQUEST)
    search_users_interactor = provide(SearchUsersInteractor, scope=Scope.REQUEST)
    check_subscription_status_interactor = provide(CheckSubscriptionStatusInteractor, scope=Scope.REQUEST)
    get_my_subscriptions_interactor = provide(GetMySubscriptionsInteractor, scope=Scope.REQUEST)
    get_all_channels_interactor = provide(GetAllChannelsInteractor, scope=Scope.REQUEST)

    # Media Interactors
    get_video_by_id_interactor = provide(GetVideoByIdInteractor, scope=Scope.REQUEST)
    add_view_to_video_interactor = provide(AddViewToVideoInteractor, scope=Scope.REQUEST)
    delete_video_interactor = provide(DeleteVideoInteractor, scope=Scope.REQUEST)
    edit_video_interactor = provide(EditVideoInteractor, scope=Scope.REQUEST)
    search_videos_interactor = provide(SearchVideosInteractor, scope=Scope.REQUEST)
    get_videos_by_author_interactor = provide(GetVideosByAuthorInteractor, scope=Scope.REQUEST)
    get_video_list_interactor = provide(GetVideoListInteractor, scope=Scope.REQUEST)
    upload_video_interactor = provide(UploadVideoInteractor, scope=Scope.REQUEST)
    get_user_history_interactor = provide(GetUserHistoryInteractor, scope=Scope.REQUEST)
    save_video_convert_interactor = provide(SaveVideoConvertInteractor, scope=Scope.REQUEST)
    mark_video_convert_failed_interactor = provide(MarkVideoConvertFailedInteractor, scope=Scope.REQUEST)
