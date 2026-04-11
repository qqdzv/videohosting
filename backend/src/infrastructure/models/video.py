from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.models.base import Base, TimestampMixin


class VideoModel(Base, TimestampMixin):
    __tablename__ = "video"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    video_url: Mapped[str | None] = mapped_column(String(500))
    preview_url: Mapped[str | None] = mapped_column(String(500))
    quality: Mapped[str | None] = mapped_column(String(50))
    duration: Mapped[float | None] = mapped_column()  # в секундах
    video_hls: Mapped[str | None] = mapped_column(String(500))
    views: Mapped[int] = mapped_column(Integer, default=0)
    process_status: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=None)
