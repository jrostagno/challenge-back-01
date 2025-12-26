import os
from datetime import datetime

import httpx

from app.domain.notification.entities import Notification
from app.domain.notification.ports.notification_sender import (
    NotificationSender,
    SendResult,
)


class HttpNotificationSender(NotificationSender):
    def __init__(self, base_url: str | None = None, timeout_seconds: float = 5.0):
        self.base_url = base_url or os.getenv(
            "DELIVERY_SERVICE_URL", "http://delivery-service:8001"
        )
        self.timeout = timeout_seconds

    async def send(self, notification: Notification) -> SendResult:
        payload = {
            "notification_id": notification.notification_id,
            "channel": notification.channel.value,
            "target": notification.target,
            "title": notification.title,
            "content": notification.content,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                r = await client.post(f"{self.base_url}/deliver", json=payload)
                r.raise_for_status()
                data = r.json()

            if data.get("status") == "sent":
                sent_at = None
                if data.get("sent_at"):
                    sent_at = datetime.fromisoformat(
                        data["sent_at"].replace("Z", "+00:00")
                    )
                return SendResult(status="sent", sent_at=sent_at)

            return SendResult(
                status="error",
                error_message=data.get("error_message", "Delivery failed"),
            )

        except Exception as e:
            return SendResult(status="error", error_message=str(e))
