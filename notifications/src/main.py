
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from dishka.integrations.faststream import setup_dishka as setup_dishka_faststream
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from faststream import FastStream
from faststream.kafka import KafkaBroker

from application.exceptions import ApplicationExceptionError
from config import settings
from controllers.handlers import router as kafka_router
from controllers.health import router as health_router
from controllers.notifications import router as notifications_router
from controllers.ws import router as ws_router
from infrastructure.resources.logging import configure_logging, get_logger
from infrastructure.resources.metrics import setup_metrics
from ioc import ApplicationProvider, DatabaseProvider, InfrastructureProvider

logger = get_logger(__name__)


def create_faststream_app() -> FastStream:
    kafka_broker = KafkaBroker(settings.kafka.server)
    faststream_app = FastStream(kafka_broker)
    kafka_broker.include_router(kafka_router)
    return faststream_app


def build_app() -> FastAPI:
    app = FastAPI(
        title="Notifications API",
        debug=settings.debug,
    )

    app.add_middleware(
        CORSMiddleware,  # ty: ignore[invalid-argument-type]
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(ws_router)
    app.include_router(notifications_router)

    setup_metrics(app)

    @app.exception_handler(ApplicationExceptionError)
    async def app_exception_handler(_request: Request, exc: ApplicationExceptionError) -> None:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_request: Request, exc: Exception) -> None:
        logger.exception("Unhandled exception", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal server error")

    return app


def configure_fastapi_app() -> FastAPI:
    configure_logging(settings.logging)

    container = make_async_container(
        DatabaseProvider(),
        InfrastructureProvider(),
        ApplicationProvider(),
    )

    faststream_app = create_faststream_app()
    fastapi_app = build_app()

    setup_dishka_faststream(container, faststream_app, auto_inject=True)
    setup_dishka_fastapi(container, fastapi_app)

    fastapi_app.add_event_handler("startup", faststream_app.start)
    fastapi_app.add_event_handler("shutdown", faststream_app.stop)

    return fastapi_app

