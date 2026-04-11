from sqlalchemy import Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.models.base import Base, TimestampMixin


class LikeModel(Base, TimestampMixin):
    __tablename__ = "like"
    __table_args__ = (
        UniqueConstraint("user_id", "video_id", name="unique_user_video_reaction"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    video_id: Mapped[int] = mapped_column(ForeignKey("video.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    is_like: Mapped[bool] = mapped_column(Boolean)  # True = like, False = dislike
