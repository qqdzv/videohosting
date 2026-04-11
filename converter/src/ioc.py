from collections.abc import AsyncIterator

import aioboto3
from dishka import Provider, Scope, provide
from faststream.kafka import KafkaBroker
from types_aiobotocore_s3 import S3Client

from application.interactors import ProcessVideoInteractor
from application.interfaces import EventPublisher, StorageService
from config import settings
from infrastructure.gateways import KafkaEventPublisher, S3StorageService


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def get_s3_session(self) -> aioboto3.Session:
        return aioboto3.Session(
            aws_access_key_id=settings.s3.access_key,
            aws_secret_access_key=settings.s3.secret_key,
            region_name=settings.s3.region_name,
        )

    @provide(scope=Scope.REQUEST)
    async def get_s3_client(
        self,
        s3_session: aioboto3.Session,
    ) -> AsyncIterator[S3Client]:
        async with s3_session.client(
            "s3",
            endpoint_url=settings.s3.endpoint_url,
        ) as client:
            yield client

    @provide(scope=Scope.APP)
    def get_event_publisher(self, kafka_broker: KafkaBroker) -> EventPublisher:
        return KafkaEventPublisher(
            broker=kafka_broker,
            config=settings.kafka,
        )

    @provide(scope=Scope.REQUEST)
    def get_storage_service(
        self,
        s3_client: S3Client,
    ) -> StorageService:
        return S3StorageService(
            s3_client=s3_client,
            bucket=settings.s3.bucket,
            public_url=settings.s3.public_url,
        )


class ApplicationProvider(Provider):
    process_video_interactor = provide(ProcessVideoInteractor, scope=Scope.REQUEST)
