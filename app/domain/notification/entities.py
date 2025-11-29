from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    ERROR = "error"


@dataclass
class Notification:
    user_id: int
    title: str
    content: str
    channel: NotificationChannel
    target: str
    status: NotificationStatus
    created_at: datetime
    updated_at: datetime
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None
    notification_id: Optional[int] = None
