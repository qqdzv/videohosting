from contextlib import asynccontextmanager

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from dishka.integrations.faststream import setup_dishka as setup_dishka_faststream
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from faststream import FastStream
from faststream.kafka import KafkaBroker

from application.exceptions import ApplicationExceptionError
from config import settings
from controllers import auth, comments, health, likes, media, subscriptions
from controllers.kafka_handlers import router as kafka_router
from infrastructure.resources.kafka import new_kafka_broker
from infrastructure.resources.logging import configure_logging, get_logger
from infrastructure.resources.metrics import setup_metrics
from ioc import (
    ApplicationProvider,
    DatabaseProvider,
    InfrastructureProvider,
    RepositoryProvider,
)

logger = get_logger(__name__)


def create_faststream_app(container: AsyncContainer, kafka_broker: KafkaBroker) -> FastStream:
    faststream_app = FastStream(kafka_broker)
    setup_dishka_faststream(container, faststream_app, auto_inject=True)
    kafka_broker.include_router(kafka_router)
    return faststream_app


def create_app() -> FastAPI:
    configure_logging(settings.logging)
    kafka_broker = new_kafka_broker(settings.kafka)
    container = make_async_container(
        DatabaseProvider(),
        RepositoryProvider(),
        InfrastructureProvider(),
        ApplicationProvider(),
        context={KafkaBroker: kafka_broker},
    )

    faststream_app = create_faststream_app(container, kafka_broker)

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        logger.info("Application starting...")
        await faststream_app.start()
        yield
        await faststream_app.stop()
        logger.info("Application stopped...")

    app = FastAPI(
        title="Video Hosting API",
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,  # ty: ignore[invalid-argument-type]
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(media.router)
    app.include_router(comments.router)
    app.include_router(likes.router)
    app.include_router(subscriptions.router)

    setup_dishka(container, app)
    setup_metrics(app)

    @app.exception_handler(ApplicationExceptionError)
    async def app_exception_handler(_request: Request, exc: ApplicationExceptionError) -> None:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_request: Request, exc: Exception) -> None:
        logger.exception("Unhandled exception", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal server error")

    return app
