
from dishka import make_async_container
from dishka.integrations.faststream import setup_dishka
from faststream import FastStream
from faststream.kafka import KafkaBroker

from config import settings
from controllers.video import router
from infrastructure.metrics import start_metrics_server
from ioc import ApplicationProvider, InfrastructureProvider

broker = KafkaBroker(settings.kafka.server)
broker.include_router(router)

container = make_async_container(
    InfrastructureProvider(),
    ApplicationProvider(),
    context={KafkaBroker: broker},
)

setup_dishka(container, broker=broker, finalize_container=False)


app = FastStream(broker)


@app.on_startup
async def on_startup() -> None:
    start_metrics_server()
