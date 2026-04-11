from sqlalchemy import JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.models.base import Base, TimestampMixin


class NotificationEventModel(Base, TimestampMixin):
    __tablename__ = "notification_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    notification_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
