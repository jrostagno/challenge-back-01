from datetime import datetime
from typing import List

from app.domain.notification.entities import Notification, NotificationUpdate
from app.domain.notification.exceptions import NotificationNotFoundError
from app.domain.notification.repository import NotificationRepository


class NotificationService:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    def create_notification(self, notification: Notification) -> Notification:
        return self.notification_repository.create_notification(notification)

    def update_notification(
        self, notification_id: int, notification: NotificationUpdate
    ) -> Notification:

        notification_to_update = self.notification_repository.get_notification_by_id(
            notification_id
        )

        if notification_to_update.user_id != notification.user_id:
            raise NotificationNotFoundError("Notification not found")

        now = datetime.now()

        notification_to_update.title = notification.title
        notification_to_update.content = notification.content
        notification_to_update.channel = notification.channel
        notification_to_update.target = notification.target
        notification_to_update.updated_at = now

        return self.notification_repository.update_notification(notification_to_update)

    def getAll_notifications(self) -> List[Notification]:
        return self.notification_repository.get_all_notifications()

    def get_notification_byID(self, notification_id: int) -> Notification | None:
        return self.notification_repository.get_notification_by_id(notification_id)

    def delete_notification(
        self,
        notification_id: int,
    ) -> Notification | None:

        return self.notification_repository.delete_notification(notification_id)
