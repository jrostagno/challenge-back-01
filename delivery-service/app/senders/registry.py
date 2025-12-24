from app.senders.base import Sender


class SenderRegistry:
    def __init__(self) -> None:
        self._senders: dict[str, Sender] = {}

    def register(self, channel: str, sender: Sender) -> None:
        self._senders[channel] = sender

    def get(self, channel: str) -> Sender:
        try:
            return self._senders[channel]
        except KeyError as err:
            raise ValueError(f"Unsupported channel: {channel}") from err
