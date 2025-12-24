from datetime import UTC, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints

Channel = Literal["email", "sms", "push"]
DeliveryStatus = Literal["pending", "sent", "error"]


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


class DeliveryRequest(BaseModel):
    notification_id: str
    target: str
    channel: Channel
    title: Annotated[str, StringConstraints(max_length=100, min_length=1)]
    content: Annotated[str, StringConstraints(max_length=1000, min_length=1)]


class DeliveryResponse(BaseModel):
    notification_id: str
    target: str
    channel: Channel
    status: DeliveryStatus
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    sent_at: datetime | None = None
    error: str | None = None
    provider_message_id: str | None = None
    details: dict[str, str] = Field(default_factory=dict)
