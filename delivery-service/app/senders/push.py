import uuid
from datetime import UTC, datetime

from app.models import DeliveryRequest, DeliveryResponse
from app.senders.base import Sender


class MockPushSender(Sender):
    async def send(self, req: DeliveryRequest) -> DeliveryResponse:
        # validación simple para challenge
        if len(req.target) < 10:
            return DeliveryResponse(
                notification_id=req.notification_id,
                channel=req.channel,
                target=req.target,
                status="error",
                error="Invalid device token",
            )

        payload = {"title": req.title, "body": req.content, "to": req.target}
        provider_id = f"mock-push-{uuid.uuid4().hex[:10]}"

        return DeliveryResponse(
            notification_id=req.notification_id,
            channel=req.channel,
            target=req.target,
            status="sent",
            sent_at=datetime.now(UTC),
            provider_message_id=provider_id,
            details={"payload_keys": ", ".join(list(payload.keys()))},
        )
