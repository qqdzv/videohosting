from typing import Protocol

from domain.entities import Comment, Like, Subscription, User, Video


class UserRepository(Protocol):
    async def find_by_id(self, user_id: int) -> User | None:
        ...

    async def find_by_email(self, email: str) -> User | None:
        ...

    async def find_by_username(self, username: str) -> User | None:
        ...

    async def search_by_username(self, query: str) -> list[User]:
        ...

    async def find_all(self) -> list[User]:
        ...

    async def create(self, user: User) -> User:
        ...

    async def update(self, user: User) -> User:
        ...

    async def delete(self, user_id: int) -> None:
        ...


class VideoRepository(Protocol):
    async def find_by_id(self, video_id: int) -> Video | None:
        ...

    async def find_all(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Video]:
        ...

    async def find_by_author(self, author_id: int) -> list[Video]:
        ...

    async def search_by_title(self, query: str) -> list[Video]:
        ...

    async def create(self, video: Video) -> Video:
        ...

    async def update(self, video: Video) -> Video:
        ...

    async def delete(self, video_id: int) -> None:
        ...

    async def increment_views(self, video_id: int) -> None:
        ...

    async def add_to_history(self, user_id: int, video_id: int) -> None:
        ...

    async def get_user_history(self, user_id: int) -> list[Video]:
        ...


class CommentRepository(Protocol):
    async def find_by_id(self, comment_id: int) -> Comment | None:
        ...

    async def find_by_video(self, video_id: int) -> list[Comment]:
        ...

    async def create(self, comment: Comment) -> Comment:
        ...

    async def update(self, comment: Comment) -> Comment:
        ...

    async def delete(self, comment_id: int) -> None:
        ...


class LikeRepository(Protocol):
    async def find_by_user_and_video(
        self,
        user_id: int,
        video_id: int,
    ) -> Like | None:
        ...

    async def count_likes(self, video_id: int) -> int:
        ...

    async def count_dislikes(self, video_id: int) -> int:
        ...

    async def get_user_reaction(self, video_id: int, user_id: int) -> str | None:
        ...

    async def create(self, like: Like) -> Like:
        ...

    async def update(self, like: Like) -> Like:
        ...

    async def delete(self, like_id: int) -> None:
        ...


class SubscriptionRepository(Protocol):
    async def find_by_id(self, subscription_id: int) -> Subscription | None:
        ...

    async def find_by_subscriber_and_author(
        self,
        subscriber_id: int,
        author_id: int,
    ) -> Subscription | None:
        ...

    async def find_by_subscriber(self, subscriber_id: int) -> list[Subscription]:
        ...

    async def find_by_author(self, author_id: int) -> list[Subscription]:
        ...

    async def count_subscribers(self, author_id: int) -> int:
        ...

    async def create(self, subscription: Subscription) -> Subscription:
        ...

    async def delete(self, subscription_id: int) -> None:
        ...
