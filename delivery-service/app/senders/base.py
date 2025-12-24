from abc import ABC, abstractmethod

from app.models import DeliveryRequest, DeliveryResponse


class Sender(ABC):
    @abstractmethod
    async def send(self, request: DeliveryRequest) -> DeliveryResponse:
        pass
