import uuid
from datetime import UTC, datetime

from app.models import DeliveryRequest, DeliveryResponse
from app.senders.base import Sender


class MockSmsSender(Sender):
    async def send(self, req: DeliveryRequest) -> DeliveryResponse:
        content = req.content
        truncated = False
        if len(content) > 160:
            content = content[:160]
            truncated = True

        provider_id = f"mock-sms-{uuid.uuid4().hex[:10]}"

        return DeliveryResponse(
            notification_id=req.notification_id,
            channel=req.channel,
            target=req.target,
            status="sent",
            sent_at=datetime.now(UTC),
            provider_message_id=provider_id,
            details={
                "truncated": str(truncated),
                "final_length": str(len(content)),
                "phone": req.target,
            },
        )
