from dataclasses import dataclass
from datetime import datetime


@dataclass
class RegisterUserDTO:
    first_name: str
    last_name: str
    username: str
    email: str
    password: str


@dataclass
class LoginUserDTO:
    email: str
    password: str


@dataclass
class JwtTokenDTO:
    access_token: str
    token_type: str = "bearer"  # noqa: S105


@dataclass
class CreateVideoDTO:
    title: str
    description: str | None
    author_id: int


@dataclass
class UpdateVideoDTO:
    title: str | None = None
    description: str | None = None


@dataclass
class UploadVideoDTO:
    video_id: int
    file_content: bytes
    filename: str
    content_type: str | None = None


@dataclass
class AuthorViewDTO:
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    total_subscribers: int = 0
    avatar: str | None = None


@dataclass
class VideoDetailDTO:
    id: int
    title: str | None
    description: str | None
    video_url: str | None
    preview_url: str | None
    quality: str | None
    duration: float | None
    video_hls: str | None
    views: int | None
    author: AuthorViewDTO
    reaction: str | None  # "like", "dislike" или None
    process_status: bool | None
    likes: int | None
    dislikes: int | None
    created_at: datetime | None


@dataclass
class VideoListItemDTO:
    id: int
    title: str
    preview_url: str | None
    duration: int | None
    views: int
    created_at: datetime
    author_username: str


@dataclass
class CreateCommentDTO:
    video_id: int
    author_id: int
    text: str


@dataclass
class CommentDTO:
    id: int
    video_id: int
    author_id: int
    username: str
    first_name: str | None
    last_name: str | None
    avatar: str | None
    text: str
    created_at: datetime


@dataclass
class CreateLikeDTO:
    video_id: int
    user_id: int
    is_like: bool  # True = like, False = dislike


@dataclass
class LikeStatsDTO:
    video_id: int
    likes_count: int
    dislikes_count: int
    user_reaction: str | None  # "like", "dislike" или None


@dataclass
class CreateSubscriptionDTO:
    subscriber_id: int
    author_id: int


@dataclass
class SubscriptionDTO:
    id: int
    subscriber_id: int
    author_id: int
    author_username: str
    created_at: datetime


@dataclass
class UserProfileDTO:
    first_name: str | None
    last_name: str | None
    username: str
    email: str
    total_subscribers: int = 0
    avatar: str | None = None


@dataclass
class UpdateUserProfileDTO:
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: str | None = None


@dataclass
class AvatarPresignedUrlDTO:
    presigned_url: str
    key: str


@dataclass
class UpdateAvatarDTO:
    key: str


@dataclass
class SuccessResponseDTO:
    success: bool = True


@dataclass
class UploadFileResponseDTO:
    public_url: str


@dataclass
class UploadVideoRequestDTO:
    title: str
    description: str
    file_content: bytes
    filename: str
    content_type: str | None = None


@dataclass
class SearchVideosRequestDTO:
    query: str


@dataclass
class UpdateCommentDTO:
    text: str


@dataclass
class SetReactionDTO:
    reaction: str  # "like" или "dislike"


@dataclass
class AuthorDTO:
    id: int
    username: str
    first_name: str | None
    last_name: str | None
    avatar: str | None
    total_subscribers: int
