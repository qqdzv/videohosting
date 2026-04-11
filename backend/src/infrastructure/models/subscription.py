from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.models.base import Base, TimestampMixin


class SubscriptionModel(Base, TimestampMixin):
    __tablename__ = "subscription"
    __table_args__ = (
        UniqueConstraint(
            "subscriber_id",
            "author_id",
            name="unique_subscriber_author",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    subscriber_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
