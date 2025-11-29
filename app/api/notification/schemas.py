from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.domain.notification.entities import NotificationChannel, NotificationStatus


class NotificationBase(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="The title of the notification",
        examples=["Pending payment!"],
    )
    content: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="The content of the notification",
        examples=["Your payment of $100 is due on December 1st."],
    )
    channel: NotificationChannel = Field(
        ...,
        description="Channel used to send the notification",
        examples=["email"],
    )
    target: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="The target of the notification",
        examples=["john.doe@example.com"],
    )


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
    ent_at: Optional[datetime] = None
    error_message: Optional[str] = None
