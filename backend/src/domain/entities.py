from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int | None
    username: str
    email: str
    hashed_password: str
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: str | None = None
    created_at: datetime | None = None


@dataclass
class Video:
    id: int | None
    title: str
    description: str | None
    author_id: int
    video_url: str | None = None
    preview_url: str | None = None
    quality: str | None = None
    duration: float | None = None  # в секундах
    video_hls: str | None = None
    views: int = 0
    process_status: bool | None = None  # статус обработки видео
    created_at: datetime | None = None


@dataclass
class Comment:
    id: int | None
    video_id: int
    author_id: int
    text: str
    created_at: datetime | None = None


@dataclass
class Like:
    id: int | None
    video_id: int
    user_id: int
    is_like: bool  # True = like, False = dislike
    created_at: datetime | None = None


@dataclass
class Subscription:
    id: int | None
    subscriber_id: int  # кто подписался
    author_id: int  # на кого подписались
    created_at: datetime | None = None
