from dataclasses import dataclass


@dataclass(frozen=True)
class DomainEvent:
    pass


@dataclass(frozen=True)
class UserCreatedEvent(DomainEvent):
    user_id: int
    email: str
    username: str


@dataclass(frozen=True)
class UserLoggedInEvent(DomainEvent):
    user_id: int
    email: str
    username: str


@dataclass(frozen=True)
class UserLoggedOutEvent(DomainEvent):
    user_id: int


@dataclass(frozen=True)
class SubscriptionCreatedEvent(DomainEvent):
    user_id: int
    email: str
    username: str
    follower: str


@dataclass(frozen=True)
class CommentCreatedEvent(DomainEvent):
    user_id: int
    email: str
    username: str
    comment: str
    sender: str


@dataclass(frozen=True)
class VideoConvertStartEvent(DomainEvent):
    id: int
    video_url: str


@dataclass(frozen=True)
class VideoPublishedEvent(DomainEvent):
    user_id: int
    email: str
    username: str
    title: str
    author: str
