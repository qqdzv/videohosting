import json

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect

from application.interfaces import CacheService, WebSocketService
from infrastructure.resources.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.websocket("/ws/{ticket}")
@inject
async def ws_connect(
    websocket: WebSocket,
    ticket: str,
    cache_service: FromDishka[CacheService],
    ws_service: FromDishka[WebSocketService],
) -> None:
    data = await cache_service.get(f"ws_ticket:{ticket}")
    if not data:
        await websocket.close(code=4001)
        return
    await cache_service.delete(f"ws_ticket:{ticket}")
    user_id = int(json.loads(data)["user_id"])
    await ws_service.connect(websocket=websocket, user_id=user_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    except Exception:
        logger.exception("WebSocket error", user_id=user_id)
