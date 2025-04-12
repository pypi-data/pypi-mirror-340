from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass

from logicblocks.event.types import EventSourceIdentifier


@dataclass(frozen=True)
class EventSubscriptionSourceMapping:
    subscriber_group: str
    event_sources: Sequence[EventSourceIdentifier]


class EventSubscriptionSourceMappingStore(ABC):
    @abstractmethod
    async def add(
        self,
        subscriber_group: str,
        event_sources: Sequence[EventSourceIdentifier],
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def remove(self, subscriber_group: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def list(self) -> Sequence[EventSubscriptionSourceMapping]:
        raise NotImplementedError()
