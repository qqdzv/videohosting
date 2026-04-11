from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.repositories import (
    CommentRepository,
    LikeRepository,
    SubscriptionRepository,
    UserRepository,
    VideoRepository,
)
from domain.entities import Comment, Like, Subscription, User, Video
from infrastructure.models import (
    CommentModel,
    HistoryModel,
    LikeModel,
    SubscriptionModel,
    UserModel,
    VideoModel,
)


class SqlUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, user_id: int) -> User | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_username(self, username: str) -> User | None:
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def search_by_username(self, query: str) -> list[User]:
        stmt = select(UserModel).where(UserModel.username.ilike(f"%{query}%"))
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def find_all(self) -> list[User]:
        stmt = select(UserModel)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def create(self, user: User) -> User:
        model = self._to_model(user)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def update(self, user: User) -> User:
        stmt = select(UserModel).where(UserModel.id == user.id)
        result = await self._session.execute(stmt)
        model = result.scalar_one()

        model.username = user.username
        model.email = user.email
        model.hashed_password = user.hashed_password
        model.first_name = user.first_name
        model.last_name = user.last_name
        model.avatar = user.avatar_url

        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, user_id: int) -> None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        await self._session.delete(model)
        await self._session.flush()

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            first_name=model.first_name,
            last_name=model.last_name,
            avatar_url=model.avatar,
            created_at=model.created_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            hashed_password=entity.hashed_password,
            first_name=entity.first_name,
            last_name=entity.last_name,
            avatar=entity.avatar_url,
        )


class SqlVideoRepository(VideoRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, video_id: int) -> Video | None:
        stmt = select(VideoModel).where(VideoModel.id == video_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_all(self, limit: int = 100, offset: int = 0) -> list[Video]:
        stmt = select(VideoModel).where(VideoModel.process_status.is_(True)).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def create(self, video: Video) -> Video:
        model = self._to_model(video)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def update(self, video: Video) -> Video:
        stmt = select(VideoModel).where(VideoModel.id == video.id)
        result = await self._session.execute(stmt)
        model = result.scalar_one()

        model.title = video.title
        model.description = video.description
        model.video_url = video.video_url
        model.preview_url = video.preview_url
        model.duration = video.duration
        model.quality = video.quality
        model.video_hls = video.video_hls
        model.process_status = video.process_status
        model.views = video.views

        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, video_id: int) -> None:
        stmt = select(VideoModel).where(VideoModel.id == video_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        await self._session.delete(model)
        await self._session.flush()

    async def increment_views(self, video_id: int) -> None:
        stmt = (
            update(VideoModel)
            .where(VideoModel.id == video_id)
            .values(views=VideoModel.views + 1)
        )
        await self._session.execute(stmt)
        await self._session.flush()

    async def find_by_author(self, author_id: int) -> list[Video]:
        stmt = (
            select(VideoModel)
            .where(VideoModel.author_id == author_id)
            .order_by(VideoModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def search_by_title(self, query: str) -> list[Video]:
        stmt = select(VideoModel).where(VideoModel.process_status.is_(True)).where(VideoModel.title.ilike(f"%{query}%"))
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def add_to_history(self, user_id: int, video_id: int) -> None:
        await self._session.execute(
            delete(HistoryModel).where(
                HistoryModel.user_id == user_id,
                HistoryModel.video_id == video_id,
            ),
        )
        self._session.add(HistoryModel(user_id=user_id, video_id=video_id))
        await self._session.flush()

    async def get_user_history(self, user_id: int) -> list[Video]:
        stmt = (
            select(VideoModel)
            .join(HistoryModel, HistoryModel.video_id == VideoModel.id)
            .where(HistoryModel.user_id == user_id)
            .order_by(HistoryModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    def _to_entity(self, model: VideoModel) -> Video:
        return Video(
            id=model.id,
            title=model.title,
            description=model.description,
            author_id=model.author_id,
            video_url=model.video_url,
            preview_url=model.preview_url,
            quality=model.quality,
            duration=model.duration,
            video_hls=model.video_hls,
            views=model.views,
            process_status=model.process_status,
            created_at=model.created_at,
        )

    def _to_model(self, entity: Video) -> VideoModel:
        return VideoModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            author_id=entity.author_id,
            video_url=entity.video_url,
            preview_url=entity.preview_url,
            quality=entity.quality,
            duration=entity.duration,
            video_hls=entity.video_hls,
            views=entity.views,
            process_status=entity.process_status,
        )


class SqlCommentRepository(CommentRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, comment_id: int) -> Comment | None:
        stmt = select(CommentModel).where(CommentModel.id == comment_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_video(self, video_id: int) -> list[Comment]:
        stmt = (
            select(CommentModel)
            .where(CommentModel.video_id == video_id)
            .order_by(CommentModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def create(self, comment: Comment) -> Comment:
        model = self._to_model(comment)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def update(self, comment: Comment) -> Comment:
        stmt = select(CommentModel).where(CommentModel.id == comment.id)
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.text = comment.text
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, comment_id: int) -> None:
        stmt = select(CommentModel).where(CommentModel.id == comment_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        await self._session.delete(model)
        await self._session.flush()

    def _to_entity(self, model: CommentModel) -> Comment:
        return Comment(
            id=model.id,
            video_id=model.video_id,
            author_id=model.author_id,
            text=model.text,
            created_at=model.created_at,
        )

    def _to_model(self, entity: Comment) -> CommentModel:
        return CommentModel(
            id=entity.id,
            video_id=entity.video_id,
            author_id=entity.author_id,
            text=entity.text,
        )


class SqlLikeRepository(LikeRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_user_and_video(self, user_id: int, video_id: int) -> Like | None:
        stmt = select(LikeModel).where(
            LikeModel.user_id == user_id,
            LikeModel.video_id == video_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def count_likes(self, video_id: int) -> int:
        stmt = select(func.count()).where(
            LikeModel.video_id == video_id,
            LikeModel.is_like.is_(True),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def count_dislikes(self, video_id: int) -> int:
        stmt = select(func.count()).where(
            LikeModel.video_id == video_id,
            LikeModel.is_like.is_(False),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def get_user_reaction(self, video_id: int, user_id: int) -> str | None:
        stmt = select(LikeModel).where(
            LikeModel.video_id == video_id,
            LikeModel.user_id == user_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return "like" if model.is_like else "dislike"

    async def create(self, like: Like) -> Like:
        model = self._to_model(like)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def update(self, like: Like) -> Like:
        stmt = select(LikeModel).where(LikeModel.id == like.id)
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.is_like = like.is_like
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, like_id: int) -> None:
        stmt = select(LikeModel).where(LikeModel.id == like_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        await self._session.delete(model)
        await self._session.flush()

    def _to_entity(self, model: LikeModel) -> Like:
        return Like(
            id=model.id,
            video_id=model.video_id,
            user_id=model.user_id,
            is_like=model.is_like,
        )

    def _to_model(self, entity: Like) -> LikeModel:
        return LikeModel(
            id=entity.id,
            video_id=entity.video_id,
            user_id=entity.user_id,
            is_like=entity.is_like,
        )


class SqlSubscriptionRepository(SubscriptionRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, subscription_id: int) -> Subscription | None:
        stmt = select(SubscriptionModel).where(SubscriptionModel.id == subscription_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_subscriber_and_author(
        self,
        subscriber_id: int,
        author_id: int,
    ) -> Subscription | None:
        stmt = select(SubscriptionModel).where(
            SubscriptionModel.subscriber_id == subscriber_id,
            SubscriptionModel.author_id == author_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_subscriber(self, subscriber_id: int) -> list[Subscription]:
        stmt = select(SubscriptionModel).where(
            SubscriptionModel.subscriber_id == subscriber_id,
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def find_by_author(self, author_id: int) -> list[Subscription]:
        stmt = select(SubscriptionModel).where(
            SubscriptionModel.author_id == author_id,
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def count_subscribers(self, author_id: int) -> int:
        stmt = select(func.count()).where(SubscriptionModel.author_id == author_id)
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def create(self, subscription: Subscription) -> Subscription:
        model = self._to_model(subscription)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, subscription_id: int) -> None:
        stmt = select(SubscriptionModel).where(SubscriptionModel.id == subscription_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        await self._session.delete(model)
        await self._session.flush()

    def _to_entity(self, model: SubscriptionModel) -> Subscription:
        return Subscription(
            id=model.id,
            subscriber_id=model.subscriber_id,
            author_id=model.author_id,
        )

    def _to_model(self, entity: Subscription) -> SubscriptionModel:
        return SubscriptionModel(
            id=entity.id,
            subscriber_id=entity.subscriber_id,
            author_id=entity.author_id,
        )
