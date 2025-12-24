import re
import uuid
from datetime import UTC, datetime

from app.models import DeliveryRequest, DeliveryResponse
from app.senders.base import Sender

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class MockEmailSender(Sender):
    async def send(self, req: DeliveryRequest) -> DeliveryResponse:
        if not EMAIL_RE.match(req.target):
            return DeliveryResponse(
                notification_id=req.notification_id,
                channel=req.channel,
                target=req.target,
                status="error",
                error="Invalid email format",
            )

        template = f"""Hola,

{req.title}

{req.content}

Saludos.
"""
        provider_id = f"mock-email-{uuid.uuid4().hex[:10]}"

        return DeliveryResponse(
            notification_id=req.notification_id,
            channel=req.channel,
            target=req.target,
            status="sent",
            sent_at=datetime.now(UTC),
            provider_message_id=provider_id,
            details={
                "template": "default_v1",
                "preview": template[:60],
            },
        )
