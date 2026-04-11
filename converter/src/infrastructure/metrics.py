from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from prometheus_client import Counter, Gauge, Histogram, start_http_server

from config import settings

MESSAGES_TOTAL = Counter(
    "converter_messages_total",
    "Total Kafka messages processed",
    ["status"],
)

PROCESSING_DURATION = Histogram(
    "converter_processing_duration_seconds",
    "Time spent processing a message",
    buckets=(1, 5, 10, 30, 60, 120, 300, 600),
)

MESSAGES_IN_PROGRESS = Gauge(
    "converter_messages_in_progress",
    "Number of messages currently being processed",
)


def start_metrics_server() -> None:
    start_http_server(settings.metrics.port)


@asynccontextmanager
async def track_message() -> AsyncIterator[None]:
    MESSAGES_IN_PROGRESS.inc()
    with PROCESSING_DURATION.time():
        try:
            yield
            MESSAGES_TOTAL.labels(status="success").inc()
        except Exception:
            MESSAGES_TOTAL.labels(status="error").inc()
            raise
        finally:
            MESSAGES_IN_PROGRESS.dec()
