from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.notification.entities import NotificationChannel, NotificationStatus
from app.infraestructure.db.base import Base


class NotificationORM(Base):
    __tablename__ = "notifications"

    notification_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), index=True
    )
    channel: Mapped[NotificationChannel] = mapped_column(String, index=True)
    target: Mapped[str] = mapped_column(String, index=True)
    content: Mapped[str] = mapped_column(String, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[NotificationStatus] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now, index=True)
    sent_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, index=True)
    error_message: Mapped[str] = mapped_column(String, nullable=True, index=True)
