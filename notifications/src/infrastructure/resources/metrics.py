from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator


def setup_metrics(app: FastAPI) -> None:
    Instrumentator(should_group_status_codes=False).instrument(app).expose(app)
