from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    ERROR = "error"


@dataclass
class NotificationUpdate:
    user_id: int
    title: str
    content: str
    channel: NotificationChannel
    target: str


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
    sent_at: datetime | None = None
    error_message: str | None = None
    notification_id: int | None = None
