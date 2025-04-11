from typing import Any
from typing import AsyncGenerator
from typing import Dict
from typing import Generator
from typing import List
from typing import Union

from pydantic import ConfigDict

from grafi.common.events.event import EventType
from grafi.common.events.topic_events.publish_to_topic_event import PublishToTopicEvent
from grafi.common.models.message import Message


class OutputTopicEvent(PublishToTopicEvent):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    event_type: EventType = EventType.OUTPUT_TOPIC
    data: Union[
        Message,
        List[Message],
        Generator[Message, None, None],
        AsyncGenerator[Message, None],
    ]

    def to_dict(self):
        # TODO: Implement serialization for `data` field
        if isinstance(self.data, Generator) or isinstance(self.data, AsyncGenerator):
            return {
                **super().to_dict(),
                "data": None,
            }
        else:
            return super().to_dict()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        # TODO: Implement deserialization for `data` field
        return super().from_dict(data)
