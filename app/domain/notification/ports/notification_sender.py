from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Protocol

from app.domain.notification.entities import Notification


@dataclass(frozen=True)
class SendResult:
    status: Literal["sent", "error"]
    sent_at: datetime | None = None
    error_message: str | None = None


class NotificationSender(Protocol):
    async def send(self, notification: Notification) -> SendResult: ...
