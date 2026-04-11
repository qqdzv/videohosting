from datetime import datetime

from pydantic import BaseModel


class UserCreatedSchema(BaseModel):
    user_id: int
    email: str
    username: str


class UserLoginedSchema(BaseModel):
    user_id: int
    email: str
    username: str


class CommentCreatedSchema(BaseModel):
    user_id: int
    email: str
    username: str
    comment: str
    sender: str


class SubscriptionCreatedSchema(BaseModel):
    user_id: int
    email: str
    username: str
    follower: str


class VideoPublishedSchema(BaseModel):
    user_id: int
    email: str
    username: str
    title: str
    author: str


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: str
    message: str
    is_read: bool
    created_at: datetime


class NotificationsListResponse(BaseModel):
    unread: int
    data: list[NotificationResponse]
