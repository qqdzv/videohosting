from dataclasses import dataclass

from application.dto import CommentDTO, CreateCommentDTO, UpdateCommentDTO
from application.events import CommentCreatedEvent
from application.exceptions import CommentNotFoundError, NotYourCommentError
from application.interfaces.gateways import EventPublisher
from application.interfaces.repositories import (
    CommentRepository,
    UserRepository,
    VideoRepository,
)
from application.interfaces.unit_of_work import UnitOfWork
from domain.entities import Comment
from infrastructure.resources.logging import get_logger

logger = get_logger(__name__)


@dataclass
class CreateCommentInteractor:
    _comment_repository: CommentRepository
    _video_repository: VideoRepository
    _user_repository: UserRepository
    _event_publisher: EventPublisher
    _uow: UnitOfWork

    async def execute(self, data: CreateCommentDTO) -> Comment:
        async with self._uow:
            comment = Comment(
                id=None,
                video_id=data.video_id,
                author_id=data.author_id,
                text=data.text,
            )

            comment = await self._comment_repository.create(comment)

            video = await self._video_repository.find_by_id(data.video_id)
            video_author = await self._user_repository.find_by_id(video.author_id)
            comment_author = await self._user_repository.find_by_id(data.author_id)

            await self._event_publisher.publish(
                CommentCreatedEvent(
                    user_id=video_author.id,
                    email=video_author.email,
                    username=video_author.username,
                    comment=data.text,
                    sender=comment_author.username,
                ),
            )

            return comment


@dataclass
class DeleteCommentInteractor:
    _comment_repository: CommentRepository
    _uow: UnitOfWork

    async def execute(self, comment_id: int, user_id: int) -> None:
        async with self._uow:
            comment = await self._comment_repository.find_by_id(comment_id)
            if not comment:
                raise CommentNotFoundError(comment_id)
            if comment.author_id != user_id:
                raise NotYourCommentError

            await self._comment_repository.delete(comment_id)


@dataclass
class EditCommentInteractor:
    _comment_repository: CommentRepository
    _uow: UnitOfWork

    async def execute(self, comment_id: int, user_id: int, data: UpdateCommentDTO) -> Comment:
        async with self._uow:
            comment = await self._comment_repository.find_by_id(comment_id)
            if not comment:
                raise CommentNotFoundError(comment_id)
            if comment.author_id != user_id:
                raise NotYourCommentError

            comment.text = data.text
            return await self._comment_repository.update(comment)


@dataclass
class GetCommentsForVideoInteractor:
    _comment_repository: CommentRepository
    _user_repository: UserRepository

    async def execute(self, video_id: int) -> list[CommentDTO]:
        comments = await self._comment_repository.find_by_video(video_id)

        result = []
        for comment in comments:
            author = await self._user_repository.find_by_id(comment.author_id)
            result.append(
                CommentDTO(
                    id=comment.id,
                    video_id=comment.video_id,
                    author_id=comment.author_id,
                    username=author.username if author else "Unknown",
                    first_name=author.first_name if author else None,
                    last_name=author.last_name if author else None,
                    avatar=author.avatar_url if author else None,
                    text=comment.text,
                    created_at=comment.created_at,
                ),
            )

        return result
