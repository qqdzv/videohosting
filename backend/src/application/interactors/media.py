import random
from dataclasses import dataclass

from application.dto import (
    AuthorViewDTO,
    UpdateVideoDTO,
    UploadFileResponseDTO,
    UploadVideoRequestDTO,
    VideoDetailDTO,
)
from application.events import VideoConvertStartEvent, VideoPublishedEvent
from application.exceptions import NotYourVideoError, VideoNotFoundError
from application.interfaces.gateways import EventPublisher, StorageService
from application.interfaces.repositories import (
    LikeRepository,
    SubscriptionRepository,
    UserRepository,
    VideoRepository,
)
from application.interfaces.unit_of_work import UnitOfWork
from domain.entities import User, Video
from infrastructure.resources.logging import get_logger

logger = get_logger(__name__)


async def _build_video_detail_dto(  # noqa: PLR0913
    video: Video,
    author: User,
    likes_count: int,
    dislikes_count: int,
    user_reaction: str | None,
    subscribers_count: int,
) -> VideoDetailDTO:
    author_dto = AuthorViewDTO(
        username=author.username,
        first_name=author.first_name,
        last_name=author.last_name,
        total_subscribers=subscribers_count,
        avatar=author.avatar_url,
    )

    return VideoDetailDTO(
        id=video.id,
        title=video.title,
        description=video.description,
        video_url=video.video_url,
        preview_url=video.preview_url,
        quality=video.quality,
        duration=video.duration,
        video_hls=video.video_hls,
        views=video.views,
        author=author_dto,
        reaction=user_reaction,
        process_status=video.process_status,
        likes=likes_count,
        dislikes=dislikes_count,
        created_at=video.created_at,
    )


@dataclass
class GetVideoByIdInteractor:
    _video_repository: VideoRepository
    _user_repository: UserRepository
    _like_repository: LikeRepository
    _subscription_repository: SubscriptionRepository

    async def execute(self, video_id: int, user_id: int) -> VideoDetailDTO:
        video = await self._video_repository.find_by_id(video_id)
        if not video:
            raise VideoNotFoundError(video_id)

        author = await self._user_repository.find_by_id(video.author_id)

        likes_count = await self._like_repository.count_likes(video_id)
        dislikes_count = await self._like_repository.count_dislikes(video_id)
        user_reaction = await self._like_repository.get_user_reaction(video_id, user_id)
        subscribers_count = await self._subscription_repository.count_subscribers(video.author_id)

        return await _build_video_detail_dto(
            video=video,
            author=author,
            likes_count=likes_count,
            dislikes_count=dislikes_count,
            user_reaction=user_reaction,
            subscribers_count=subscribers_count,
        )


@dataclass
class AddViewToVideoInteractor:
    _video_repository: VideoRepository
    _uow: UnitOfWork

    async def execute(self, video_id: int, user_id: int) -> bool:
        async with self._uow:
            video = await self._video_repository.find_by_id(video_id)
            if not video:
                return False

            await self._video_repository.increment_views(video_id)

            await self._video_repository.add_to_history(user_id, video_id)

            return True


@dataclass
class DeleteVideoInteractor:
    _video_repository: VideoRepository
    _uow: UnitOfWork

    async def execute(self, video_id: int, user_id: int) -> bool:
        async with self._uow:
            video = await self._video_repository.find_by_id(video_id)
            if not video:
                raise VideoNotFoundError(video_id)

            if video.author_id != user_id:
                raise NotYourVideoError

            await self._video_repository.delete(video_id)
            return True


@dataclass
class EditVideoInteractor:
    _video_repository: VideoRepository
    _uow: UnitOfWork

    async def execute(self, video_id: int, user_id: int, data: UpdateVideoDTO) -> bool:
        async with self._uow:
            video = await self._video_repository.find_by_id(video_id)
            if not video:
                raise VideoNotFoundError(video_id)

            if video.author_id != user_id:
                raise NotYourVideoError

            if data.title is not None:
                video.title = data.title
            if data.description is not None:
                video.description = data.description

            await self._video_repository.update(video)
            return True


@dataclass
class SearchVideosInteractor:
    _video_repository: VideoRepository
    _user_repository: UserRepository
    _like_repository: LikeRepository
    _subscription_repository: SubscriptionRepository

    async def execute(self, query: str, user_id: int) -> list[VideoDetailDTO]:
        videos = await self._video_repository.search_by_title(query)

        result = []
        for video in videos:
            author = await self._user_repository.find_by_id(video.author_id)
            likes_count = await self._like_repository.count_likes(video.id)
            dislikes_count = await self._like_repository.count_dislikes(video.id)
            user_reaction = await self._like_repository.get_user_reaction(video.id, user_id)
            subscribers_count = await self._subscription_repository.count_subscribers(video.author_id)

            video_dto = await _build_video_detail_dto(
                video=video,
                author=author,
                likes_count=likes_count,
                dislikes_count=dislikes_count,
                user_reaction=user_reaction,
                subscribers_count=subscribers_count,
            )
            result.append(video_dto)

        return result


@dataclass
class GetVideosByAuthorInteractor:
    _video_repository: VideoRepository
    _user_repository: UserRepository
    _like_repository: LikeRepository
    _subscription_repository: SubscriptionRepository

    async def execute(self, author_username: str, user_id: int) -> list[VideoDetailDTO]:
        author = await self._user_repository.find_by_username(author_username)
        if not author:
            return []

        videos = await self._video_repository.find_by_author(author.id)

        result = []
        for video in videos:
            likes_count = await self._like_repository.count_likes(video.id)
            dislikes_count = await self._like_repository.count_dislikes(video.id)
            user_reaction = await self._like_repository.get_user_reaction(video.id, user_id)
            subscribers_count = await self._subscription_repository.count_subscribers(author.id)

            video_dto = await _build_video_detail_dto(
                video=video,
                author=author,
                likes_count=likes_count,
                dislikes_count=dislikes_count,
                user_reaction=user_reaction,
                subscribers_count=subscribers_count,
            )
            result.append(video_dto)

        return result


@dataclass
class GetVideoListInteractor:
    _video_repository: VideoRepository
    _user_repository: UserRepository
    _like_repository: LikeRepository
    _subscription_repository: SubscriptionRepository

    async def execute(
        self, user_id: int, offset: int = 0, limit: int = 100, is_random: bool = True,
    ) -> list[VideoDetailDTO]:
        videos = await self._video_repository.find_all(offset=offset, limit=limit)

        if is_random:
            random.shuffle(videos)

        result = []
        for video in videos:
            author = await self._user_repository.find_by_id(video.author_id)
            likes_count = await self._like_repository.count_likes(video.id)
            dislikes_count = await self._like_repository.count_dislikes(video.id)
            user_reaction = await self._like_repository.get_user_reaction(video.id, user_id)
            subscribers_count = await self._subscription_repository.count_subscribers(video.author_id)

            video_dto = await _build_video_detail_dto(
                video=video,
                author=author,
                likes_count=likes_count,
                dislikes_count=dislikes_count,
                user_reaction=user_reaction,
                subscribers_count=subscribers_count,
            )
            result.append(video_dto)

        return result


@dataclass
class UploadVideoInteractor:
    _video_repository: VideoRepository
    _user_repository: UserRepository
    _subscription_repository: SubscriptionRepository
    _storage_service: StorageService
    _event_publisher: EventPublisher
    _uow: UnitOfWork

    async def execute(self, data: UploadVideoRequestDTO, author_id: int) -> UploadFileResponseDTO:
        async with self._uow:
            s3_key = f"videos/{author_id}/{data.filename}"
            public_url = await self._storage_service.upload(
                file_content=data.file_content,
                file_path=s3_key,
                content_type=data.content_type,
            )

            video = Video(
                id=None,
                title=data.title,
                description=data.description,
                video_url=public_url,
                preview_url=None,
                duration=None,
                views=0,
                author_id=author_id,
                process_status=None,
            )
            video = await self._video_repository.create(video)

            await self._event_publisher.publish(
                VideoConvertStartEvent(id=video.id, video_url=s3_key),
            )

            author = await self._user_repository.find_by_id(author_id)
            subscriptions = await self._subscription_repository.find_by_author(author_id)

            for subscription in subscriptions:
                subscriber = await self._user_repository.find_by_id(subscription.subscriber_id)
                if subscriber:
                    await self._event_publisher.publish(
                        VideoPublishedEvent(
                            user_id=subscriber.id,
                            email=subscriber.email,
                            username=subscriber.username,
                            title=data.title,
                            author=author.username,
                        ),
                    )

            return UploadFileResponseDTO(public_url=public_url)


@dataclass
class GetUserHistoryInteractor:
    _video_repository: VideoRepository
    _user_repository: UserRepository
    _like_repository: LikeRepository
    _subscription_repository: SubscriptionRepository

    async def execute(self, user_id: int) -> list[VideoDetailDTO]:
        history_video_repository = await self._video_repository.get_user_history(user_id)

        result = []
        for video in history_video_repository:
            author = await self._user_repository.find_by_id(video.author_id)
            if not author:
                continue

            likes_count = await self._like_repository.count_likes(video.id)
            dislikes_count = await self._like_repository.count_dislikes(video.id)
            user_reaction = await self._like_repository.get_user_reaction(video.id, user_id)
            subscribers_count = await self._subscription_repository.count_subscribers(video.author_id)

            video_dto = await _build_video_detail_dto(
                video=video,
                author=author,
                likes_count=likes_count,
                dislikes_count=dislikes_count,
                user_reaction=user_reaction,
                subscribers_count=subscribers_count,
            )
            result.append(video_dto)

        return result


@dataclass
class SaveVideoConvertInteractor:
    _video_repository: VideoRepository
    _uow: UnitOfWork

    async def execute(
        self,
        video_id: int,
        preview_url: str,
        duration: float,
        quality: str,
        video_hls: str,
    ) -> None:
        async with self._uow:
            video = await self._video_repository.find_by_id(video_id)
            if not video:
                return

            video.preview_url = preview_url
            video.duration = duration
            video.quality = quality
            video.video_hls = video_hls
            video.process_status = True

            await self._video_repository.update(video)


@dataclass
class MarkVideoConvertFailedInteractor:
    _video_repository: VideoRepository
    _uow: UnitOfWork

    async def execute(self, video_id: int) -> None:
        async with self._uow:
            video = await self._video_repository.find_by_id(video_id)
            if not video:
                return

            video.process_status = False
            await self._video_repository.update(video)
