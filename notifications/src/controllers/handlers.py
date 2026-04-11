from dishka.integrations.fastapi import FromDishka
from dishka.integrations.faststream import inject
from faststream.kafka import KafkaRouter

from application.commands import (
    HandleCommentCreatedCommand,
    HandleCommentCreatedHandler,
    HandleSubscriptionCreatedCommand,
    HandleSubscriptionCreatedHandler,
    HandleUserCreatedCommand,
    HandleUserCreatedHandler,
    HandleVideoPublishedCommand,
    HandleVideoPublishedHandler,
)
from config import settings
from controllers.schemas import (
    CommentCreatedSchema,
    SubscriptionCreatedSchema,
    UserCreatedSchema,
    VideoPublishedSchema,
)

router = KafkaRouter()


@router.subscriber(settings.kafka.topic_user_created, max_workers=10)
@inject
async def handle_user_created(
    body: UserCreatedSchema,
    handler: FromDishka[HandleUserCreatedHandler],
) -> None:
    await handler.execute(
        HandleUserCreatedCommand(
            user_id=body.user_id,
            email=body.email,
            username=body.username,
        ),
    )


@router.subscriber(settings.kafka.topic_comment_created, max_workers=10)
@inject
async def handle_comment_created(
    body: CommentCreatedSchema,
    handler: FromDishka[HandleCommentCreatedHandler],
) -> None:
    await handler.execute(
        HandleCommentCreatedCommand(
            user_id=body.user_id,
            email=body.email,
            username=body.username,
            comment=body.comment,
            sender=body.sender,
        ),
    )


@router.subscriber(settings.kafka.topic_subscription_created, max_workers=10)
@inject
async def handle_subscription_created(
    body: SubscriptionCreatedSchema,
    handler: FromDishka[HandleSubscriptionCreatedHandler],
) -> None:
    await handler.execute(
        HandleSubscriptionCreatedCommand(
            user_id=body.user_id,
            email=body.email,
            username=body.username,
            follower=body.follower,
        ),
    )


@router.subscriber(settings.kafka.topic_video_published, max_workers=10)
@inject
async def handle_video_published(
    body: VideoPublishedSchema,
    handler: FromDishka[HandleVideoPublishedHandler],
) -> None:
    await handler.execute(
        HandleVideoPublishedCommand(
            user_id=body.user_id,
            email=body.email,
            username=body.username,
            title=body.title,
            author=body.author,
        ),
    )
