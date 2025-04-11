"""Decorator for recording tool execution events and tracing."""

import functools
import json
from typing import AsyncGenerator
from typing import List
from typing import Union

from openinference.semconv.trace import OpenInferenceSpanKindValues
from openinference.semconv.trace import SpanAttributes
from pydantic_core import to_jsonable_python

from grafi.common.containers.container import container
from grafi.common.events.tool_events.tool_event import TOOL_ID
from grafi.common.events.tool_events.tool_event import TOOL_NAME
from grafi.common.events.tool_events.tool_event import TOOL_TYPE
from grafi.common.events.tool_events.tool_failed_event import ToolFailedEvent
from grafi.common.events.tool_events.tool_invoke_event import ToolInvokeEvent
from grafi.common.events.tool_events.tool_respond_event import ToolRespondEvent
from grafi.common.instrumentations.tracing import tracer
from grafi.common.models.execution_context import ExecutionContext
from grafi.common.models.message import Message
from grafi.tools.tool import Tool


def record_tool_a_execution(func):
    """Decorator to record tool execution events and tracing."""

    @functools.wraps(func)
    async def wrapper(self: Tool, *args, **kwargs):
        tool_id: str = self.tool_id
        oi_span_type: OpenInferenceSpanKindValues = self.oi_span_type
        execution_context: ExecutionContext = (
            args[0] if args else kwargs.get("execution_context", None)
        )
        tool_name: str = self.name
        tool_type: str = self.type

        # Capture input data from args or kwargs
        input_data: Union[Message, List[Message]] = (
            args[1] if (args and len(args) > 1) else kwargs.get("input_data", "")
        )

        input_data_dict = json.dumps(input_data, default=to_jsonable_python)

        tool_event_base = {
            TOOL_ID: tool_id,
            "execution_context": execution_context,
            TOOL_TYPE: tool_type,
            TOOL_NAME: tool_name,
            "input_data": input_data,
        }

        if container.event_store:
            # Record the 'invoke' event
            invoke_event = ToolInvokeEvent(
                **tool_event_base,
            )
            container.event_store.record_event(invoke_event)

        # Execute the original function
        try:
            with tracer.start_as_current_span(f"{tool_name}.execute") as span:
                span.set_attribute(TOOL_ID, tool_id)
                span.set_attribute(TOOL_NAME, tool_name)
                span.set_attribute(TOOL_TYPE, tool_type)
                span.set_attributes(execution_context.model_dump())
                span.set_attribute("input", input_data_dict)
                span.set_attribute(
                    SpanAttributes.OPENINFERENCE_SPAN_KIND,
                    oi_span_type.value,
                )

                # Execute the original function and collect results
                async_result: AsyncGenerator[Message, None] = func(
                    self, *args, **kwargs
                )

                # If the function is a_execute, yield the results as Message
                if func.__name__ == "a_execute":
                    result = []
                    async for data in async_result:
                        result.extend(data if isinstance(data, list) else [data])
                        yield data
                else:
                    # If the function is a_stream, yield the results as a chunked string
                    result_content = ""
                    async for data in async_result:
                        if data.content is not None:
                            result_content += data.content
                        yield data

                    result = Message(role="assistant", content=result_content)

                output_data_dict = json.dumps(result, default=to_jsonable_python)

                span.set_attribute("output", output_data_dict)
        except Exception as e:
            # Exception occurred during execution
            if container.event_store:
                failed_event = ToolFailedEvent(
                    **tool_event_base,
                    error=str(e),
                )
                container.event_store.record_event(failed_event)
            raise
        else:
            # Successful execution
            if container.event_store:
                respond_event = ToolRespondEvent(
                    **tool_event_base,
                    output_data=result,
                )
                container.event_store.record_event(respond_event)

    return wrapper
