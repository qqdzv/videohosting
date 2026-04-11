from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

import aiosmtplib
import jwt
import redis.asyncio as aioredis
from fastapi import WebSocket

from application.interfaces import CacheService, EmailService, JwtService, WebSocketService


class AiosmtplibEmailService(EmailService):
    def __init__(self, host: str, port: int, username: str, password: str):
        self._host = host
        self._port = port
        self._username = username
        self._password = password

    async def send(self, to: str, subject: str, body: str) -> None:
        msg = MIMEMultipart()
        msg["From"] = self._username
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        await aiosmtplib.send(
            msg,
            hostname=self._host,
            port=self._port,
            username=self._username,
            password=self._password,
            start_tls=True,
        )


class WebSocketManager(WebSocketService):
    def __init__(self):
        self._connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int) -> None:
        await websocket.accept()
        self._connections[user_id] = websocket

    def disconnect(self, user_id: int) -> None:
        self._connections.pop(user_id, None)

    async def send(self, user_id: int, message: str) -> None:
        ws = self._connections.get(user_id)
        if ws:
            try:
                await ws.send_text(message)
            except Exception:
                self.disconnect(user_id)


class RedisCacheService(CacheService):
    def __init__(self, url: str):
        self._redis = aioredis.from_url(url, decode_responses=True)

    async def get(self, key: str) -> Any | None:
        return await self._redis.get(key)

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)


class PyJWTService(JwtService):
    def __init__(self, private_key: str, public_key: str, algorithm: str):
        self._private_key = private_key
        self._public_key = public_key
        self._algorithm = algorithm

    def decode(self, token: str) -> int | None:
        try:
            payload = jwt.decode(token, self._public_key, algorithms=[self._algorithm])
            return payload.get("id")
        except Exception:
            return None
