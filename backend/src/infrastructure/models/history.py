from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.models.base import Base


class HistoryModel(Base):
    __tablename__ = "media_history"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    video_id: Mapped[int] = mapped_column(nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
    )
