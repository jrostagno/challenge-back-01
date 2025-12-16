from datetime import datetime

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.notification.schemas import NotificationCreate, NotificationResponse
from app.domain.notification.entities import (
    Notification,
    NotificationStatus,
    NotificationUpdate,
)
from app.domain.notification.service import NotificationService
from app.infraestructure.auth.security import get_current_user
from app.infraestructure.db.session import get_session
from app.infraestructure.notification.sqlalchemy_repository import (
    SQLAlchemyNotificationRepository,
)

router = APIRouter(
    prefix="/notification",
    tags=["notifications"],
    dependencies=[Depends(get_current_user)],
)

_DEFAULT_SESSION_DEPENDENCY = Depends(get_session)


def get_notification_services(db: Session = _DEFAULT_SESSION_DEPENDENCY):
    repository = SQLAlchemyNotificationRepository(db)
    return NotificationService(repository)


_DEFAULT_NOTIFICATION_SERVICE_DEPENDENCY = Depends(get_notification_services)
_DEFAULT_CURRENT_USER_DEPENDENCY = Depends(get_current_user)


@router.post(
    "/", response_model=NotificationResponse, description="Create a notifiaction"
)
def create_notification(
    notification: NotificationCreate,
    notification_service: NotificationService = _DEFAULT_NOTIFICATION_SERVICE_DEPENDENCY,
    user: dict = _DEFAULT_CURRENT_USER_DEPENDENCY,
):
    now = datetime.now()

    print(f"User: {user}")

    new_notification = Notification(
        notification_id=None,
        user_id=user["user_id"],
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
    notification: NotificationCreate,
    notification_service: NotificationService = _DEFAULT_NOTIFICATION_SERVICE_DEPENDENCY,
    user: dict = _DEFAULT_CURRENT_USER_DEPENDENCY,
):
    notification_to_update = NotificationUpdate(
        user_id=user["user_id"],
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
    notification_service: NotificationService = _DEFAULT_NOTIFICATION_SERVICE_DEPENDENCY,
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
    notification_service: NotificationService = _DEFAULT_NOTIFICATION_SERVICE_DEPENDENCY,
):
    notification = notification_service.get_notification_byID(notification_id)
    return NotificationResponse.model_validate(notification)


@router.get(
    "/",
    response_model=list[NotificationResponse],
    description="Get all notifications",
)
def get_all_notifications(
    notification_service: NotificationService = _DEFAULT_NOTIFICATION_SERVICE_DEPENDENCY,
):
    notifications = notification_service.getAll_notifications()
    return [
        NotificationResponse.model_validate(notification)
        for notification in notifications
    ]


@router.get("/secure")
def secure_endpoint(user: dict = _DEFAULT_CURRENT_USER_DEPENDENCY):
    return {"message": "Acceso con token OK", "user": user}
