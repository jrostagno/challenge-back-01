from abc import ABC, abstractmethod
from typing import List

from app.domain.notification.entities import Notification


class NotificationRepository(ABC):
    @abstractmethod
    def create_notification(self, notification: Notification) -> Notification:
        pass

    @abstractmethod
    def update_notification(self, notification: Notification) -> Notification:
        pass

    @abstractmethod
    def delete_notification(self, notification_id: int) -> None:
        pass

    @abstractmethod
    def get_notification_by_id(self, notification_id: int) -> Notification:
        pass

    @abstractmethod
    def get_all_notifications(self) -> List[Notification]:
        pass
