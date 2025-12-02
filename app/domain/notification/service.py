from typing import List

from app.domain.notification.entities import Notification
from app.domain.notification.repository import NotificationRepository


class NotificationService:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    def create_notification(self, notification: Notification) -> Notification:
        return self.notification_repository.create_notification(notification)

    def update_notification(self, notification: Notification) -> Notification:
        return self.notification_repository.update_notification(notification)

    def getAll_notifications(self) -> List[Notification]:
        return self.notification_repository.get_all_notifications()

    def get_notification_byID(self, notification_id: int) -> Notification | None:
        return self.notification_repository.get_notification_by_id(notification_id)
