import dataclasses
from typing import Any

from faststream.kafka import KafkaBroker
from types_aiobotocore_s3 import S3Client

from application.events import DomainEvent, VideoConvertedEndEvent, VideoConvertFailedEvent
from application.interfaces import EventPublisher, MessageBroker, StorageService
from config import KafkaConfig


class KafkaMessageBroker(MessageBroker):
    def __init__(self, broker: KafkaBroker) -> None:
        self._broker = broker

    async def publish(self, message: dict[str, Any], topic: str) -> None:
        await self._broker.publish(message, topic)


class KafkaEventPublisher(EventPublisher):
    def __init__(self, broker: KafkaBroker, config: KafkaConfig) -> None:
        self._broker = broker
        self._topic_map: dict[type, str] = {
            VideoConvertedEndEvent: config.topic_video_convert_end,
            VideoConvertFailedEvent: config.topic_video_convert_error,
        }

    async def publish(self, event: DomainEvent) -> None:
        topic = self._topic_map[type(event)]
        await self._broker.publish(dataclasses.asdict(event), topic)  # ty: ignore[invalid-argument-type]


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
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type

        await self._s3.put_object(
            Bucket=self._bucket,
            Key=file_path,
            Body=file_content,
            **extra_args,
        )
        return await self.get_url(file_path)

    async def download_bytes(self, s3_path: str) -> bytes:
        response = await self._s3.get_object(Bucket=self._bucket, Key=s3_path)
        async with response["Body"] as stream:
            return await stream.read()

    async def download_file(self, s3_path: str, dest_path: str) -> None:
        await self._s3.download_file(self._bucket, s3_path, dest_path)

    async def upload_file(
        self,
        local_path: str,
        s3_path: str,
        content_type: str | None = None,
    ) -> str:
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type

        await self._s3.upload_file(local_path, self._bucket, s3_path, ExtraArgs=extra_args or None)
        return await self.get_url(s3_path)

    async def delete(self, file_path: str) -> None:
        await self._s3.delete_object(Bucket=self._bucket, Key=file_path)

    async def get_url(self, file_path: str) -> str:
        return f"{self._public_url}/{file_path}"
