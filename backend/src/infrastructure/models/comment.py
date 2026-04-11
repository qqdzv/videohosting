from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.models.base import Base, TimestampMixin


class CommentModel(Base, TimestampMixin):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    video_id: Mapped[int] = mapped_column(ForeignKey("video.id"), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    text: Mapped[str] = mapped_column(Text)
