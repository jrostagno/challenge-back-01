from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.notification.schemas import NotificationCreate, NotificationResponse
from app.domain.notification.entities import (
    Notification,
    NotificationStatus,
    NotificationUpdate,
)
from app.domain.notification.service import NotificationService
from app.infraestructure.db.session import SessionLocal
from app.infraestructure.notification.sqlalchemy_repository import (
    SQLAlchemyNotificationRepository,
)

router = APIRouter(prefix="/notification", tags=["notifications"])


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_notification_services(db: Session = Depends(get_session)):
    repository = SQLAlchemyNotificationRepository(db)
    return NotificationService(repository)


@router.post(
    "/", response_model=NotificationResponse, description="Create a notifiaction"
)
def create_notification(
    notification: NotificationCreate,
    user_id: int,
    notification_service: NotificationService = Depends(get_notification_services),
):
    now = datetime.now()

    new_notification = Notification(
        notification_id=None,
        user_id=user_id,
        title=notification.title,
        content=notification.content,
        channel=notification.channel,
        target=notification.target,
        status=NotificationStatus.PENDING,
        created_at=now,
        updated_at=now,
        sent_at=None,
        error_message=None,
    )
    created_notification = notification_service.create_notification(new_notification)

    return NotificationResponse.model_validate(created_notification)


@router.put(
    "/{notification_id}",
    response_model=NotificationResponse,
    description="Update notifiaction",
    response_description="Post actualizado con exito",
    status_code=status.HTTP_200_OK,
)
def change_notification(
    notification_id: int,
    user_id: int,
    notification: NotificationCreate,
    notification_service: NotificationService = Depends(get_notification_services),
):
    notification_to_update = NotificationUpdate(
        user_id=user_id,
        title=notification.title,
        content=notification.content,
        channel=notification.channel,
        target=notification.target,
    )
    update_notification = notification_service.update_notification(
        notification_id, notification_to_update
    )

    return NotificationResponse.model_validate(update_notification)


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete notification",
)
def delete_notification(
    notification_id: int,
    notification_service: NotificationService = Depends(get_notification_services),
):
    notification_service.delete_notification(notification_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
    description="Get notification",
)
def get_notification(
    notification_id: int,
    notification_service: NotificationService = Depends(get_notification_services),
):
    notification = notification_service.get_notification_byID(notification_id)
    return NotificationResponse.model_validate(notification)


@router.get(
    "/",
    response_model=List[NotificationResponse],
    description="Get all notifications",
)
def get_all_notifications(
    notification_service: NotificationService = Depends(get_notification_services),
):
    notifications = notification_service.getAll_notifications()
    return [
        NotificationResponse.model_validate(notification)
        for notification in notifications
    ]
