import dataclasses
import time
from typing import Any

import jwt
import redis.asyncio as aioredis
from faststream.kafka import KafkaBroker
from passlib.context import CryptContext
from types_aiobotocore_s3 import S3Client

from application.events import (
    CommentCreatedEvent,
    DomainEvent,
    SubscriptionCreatedEvent,
    UserCreatedEvent,
    UserLoggedInEvent,
    UserLoggedOutEvent,
    VideoConvertStartEvent,
    VideoPublishedEvent,
)
from application.exceptions import AuthenticationError
from application.interfaces.gateways import (
    CacheService,
    EventPublisher,
    JwtService,
    PasswordHasher,
    StorageService,
)
from config import KafkaConfig
from infrastructure.resources.logging import get_logger

logger = get_logger(__name__)


class PasslibPasswordHasher(PasswordHasher):
    def __init__(self):
        self._context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self._context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self._context.verify(plain_password, hashed_password)


class PyJWTService(JwtService):
    def __init__(self, private_key: str, public_key: str, algorithm: str, token_ttl: int):
        self._private_key = private_key
        self._public_key = public_key
        self._algorithm = algorithm
        self._token_ttl = token_ttl

    def create_token(self, payload: dict[str, Any]) -> str:
        payload["exp"] = int(time.time()) + self._token_ttl
        return jwt.encode(payload, self._private_key, algorithm=self._algorithm)

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, self._public_key, algorithms=[self._algorithm])
        except jwt.PyJWTError as err:
            raise AuthenticationError from err


class RedisCacheService(CacheService):
    def __init__(self, url: str):
        self._redis = aioredis.from_url(url, decode_responses=True)

    async def get(self, key: str) -> Any | None:
        return await self._redis.get(key)

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        await self._redis.set(key, value, ex=ttl)

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)

    async def exists(self, key: str) -> bool:
        return await self._redis.exists(key) > 0


class KafkaEventPublisher(EventPublisher):
    def __init__(self, broker: KafkaBroker, config: KafkaConfig):
        self._broker = broker
        self._topic_map: dict[type, str] = {
            UserCreatedEvent: config.topic_user_created,
            UserLoggedInEvent: config.topic_user_logged_in,
            UserLoggedOutEvent: config.topic_user_logged_out,
            SubscriptionCreatedEvent: config.topic_subscription_created,
            CommentCreatedEvent: config.topic_comment_created,
            VideoConvertStartEvent: config.topic_video_convert_start,
            VideoPublishedEvent: config.topic_video_published,
        }

    async def publish(self, event: DomainEvent) -> None:
        topic = self._topic_map[type(event)]
        try:
            event_dict = dataclasses.asdict(event)
            await self._broker.publish(event_dict, topic)
            logger.info("Kafka Publish Event", event_type=type(event).__name__, data=event_dict)
        except Exception:
            logger.exception("Failed to publish event", event_type=type(event).__name__)


class S3StorageService(StorageService):
    def __init__(
        self,
        s3_client: S3Client,
        bucket: str,
        public_url: str,
    ):
        self._s3 = s3_client
        self._bucket = bucket
        self._public_url = public_url

    async def upload(
        self,
        file_content: bytes,
        file_path: str,
        content_type: str | None = None,
    ) -> str:
        extra_args: dict = {}
        if content_type:
            extra_args["ContentType"] = content_type

        await self._s3.put_object(
            Bucket=self._bucket,
            Key=file_path,
            Body=file_content,
            **extra_args,
        )
        return await self.get_url(file_path)

    async def delete(self, file_path: str) -> None:
        await self._s3.delete_object(Bucket=self._bucket, Key=file_path)

    async def get_url(self, file_path: str) -> str:
        return f"{self._public_url}/{file_path}"

    async def generate_presigned_upload_url(
        self,
        key: str,
        content_type: str,
        expires_in: int = 600,
    ) -> str:
        await self._s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self._bucket,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=expires_in,
        )
        return await self.get_url(file_path=key)
