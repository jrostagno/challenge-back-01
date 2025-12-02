from typing import Optional

from sqlalchemy.orm import Session

from app.domain.notification.entities import Notification
from app.domain.notification.repository import NotificationRepository
from app.infraestructure.db.models.notification_model import NotificationORM


class SQLAlchemyNotificationRepository(NotificationRepository):
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def to_domain(orm: NotificationORM) -> Notification:
        return Notification(
            notification_id=orm.notification_id,
            user_id=orm.user_id,
            title=orm.title,
            content=orm.content,
            channel=orm.channel,
            status=orm.status,
            target=orm.target,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            sent_at=orm.sent_at,
            error_message=orm.error_message,
        )

    def create_notification(self, notification: Notification) -> Notification:
        notification_orm = NotificationORM(
            user_id=notification.user_id,
            title=notification.title,
            content=notification.content,
            channel=notification.channel,
            status=notification.status,
            target=notification.target,
            created_at=notification.created_at,
            updated_at=notification.updated_at,
            sent_at=notification.sent_at,
            error_message=notification.error_message,
        )

        self.session.add(notification_orm)
        self.session.commit()
        self.session.refresh(notification_orm)

        return self.to_domain(notification_orm)

    def update_notification(self, notification: Notification) -> Notification:

        notification_to_update: Optional[NotificationORM] = self.session.get(
            NotificationORM, notification.notification_id
        )

        if notification_to_update is None:

            raise ValueError(
                f"Notification with id {notification.notification_id} not found"
            )

        notification_to_update.title = notification.title
        notification_to_update.content = notification.content
        notification_to_update.channel = notification.channel
        notification_to_update.status = notification.status
        notification_to_update.target = notification.target
        notification_to_update.updated_at = notification.updated_at
        notification_to_update.sent_at = notification.sent_at  # type: ignore[assignment]
        notification_to_update.error_message = notification.error_message  # type: ignore[assignment]

        self.session.commit()
        self.session.refresh(notification_to_update)

        return self.to_domain(notification_to_update)

    def delete_notification(self, notification_id: int) -> None:
        notification_to_delete: Optional[NotificationORM] = self.session.get(
            NotificationORM, notification_id
        )

        if notification_to_delete is None:
            raise ValueError(f"Notification with id {notification_id} not found")

        self.session.delete(notification_to_delete)
        self.session.commit()
