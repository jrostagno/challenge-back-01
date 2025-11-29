from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class NotificationsChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "error"


class NotificationBase(BaseModel):
    title: str
    content: str
    channel: NotificationsChannel
    target: str


class NotificationCreate(NotificationBase):
    pass


class NotificationInDB(NotificationBase):
    notification_id: int
    user_id: int
    status: NotificationStatus
    created_at: datetime
    updated_at: datetime
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class NotificationResponse(NotificationBase):
    notification_id: int
    status: NotificationStatus
    user_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
