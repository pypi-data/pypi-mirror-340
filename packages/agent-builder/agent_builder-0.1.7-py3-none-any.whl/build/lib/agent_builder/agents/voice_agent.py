"""
VoiceAgent Module

This module provides the `VoiceAgent` class, which is designed for voice
interactions with the OpenAI Realtime API. The agent manages audio input/output streams,
handles tool execution, and processes events according to the OpenAI Realtime API specifications.

**Event Handling:**

The `VoiceAgent` communicates with the OpenAI Realtime API WebSocket server.
The sequence of events is as follows:

1. **Session Initialization**:
   - The agent sends a `session.update` event to configure the session,
   including instructions, voice settings, tools, and other parameters.
   - The server responds with `session.created` and `session.updated` events.

2. **Input Audio Handling**:
   - The agent receives audio input from the user and sends `input_audio_buffer.append`
   events to the server.
   - If server-side VAD (Voice Activity Detection) is enabled, the server detects
   speech start and stop, sending `input_audio_buffer.speech_started` and
   `input_audio_buffer.speech_stopped` events.
   - Upon speech stop, the server commits the audio buffer and sends
   an `input_audio_buffer.committed` event.

3. **Response Generation**:
   - The agent may send a `response.create` event to trigger response generation.
   - The server generates responses, which may include text, audio, or function calls.
   - The server sends events such as `response.created`, `response.audio.delta`,
   `response.audio.done`, `response.function_call_arguments.done`, and `response.done`.

4. **Function Call Handling**:
   - If the assistant invokes a tool, the server sends a
   `response.function_call_arguments.done` event with the tool call details.
   - The agent executes the tool and sends a `conversation.item.create` event with the result.
   - The agent may then send a `response.create` event to continue the conversation.

5. **Event Types and Ignored Events**:
   - The agent handles specific event types and ignores others as defined by the `EVENTS_TO_IGNORE` set.

Refer to the OpenAI Realtime API documentation for detailed information
on the event structures and sequences: https://platform.openai.com/docs/api-reference/realtime
"""

import asyncio
import json
import logging
from typing import Any, AsyncIterator, Callable, Coroutine, Dict, List, Optional, Tuple

from langchain_core.tools import BaseTool
from agent_builder.utils.websocket_connection import websocket_connection
from agent_builder.utils.call_end_exception import CallEndException

# Event types constants
from agent_builder.config.default import (
    SESSION_UPDATE,
    RESPONSE_CREATE,
    RESPONSE_CANCEL,
    CONVERSATION_ITEM_CREATE,
    INPUT_AUDIO_BUFFER_APPEND,
    RESPONSE_AUDIO_DELTA,
    RESPONSE_AUDIO_DONE,
    RESPONSE_FUNCTION_CALL_ARGUMENTS_DONE,
    INPUT_AUDIO_BUFFER_SPEECH_STARTED,
    ERROR,
    INPUT_AUDIO_TRANSCRIPTION_COMPLETED,
    RESPONSE_AUDIO_TRANSCRIPT_DONE,
    EVENTS_TO_IGNORE,
    CALL_END,
)


class VoiceAgent:
    """
    A voice interaction agent that manages audio input/output streams and tool execution.

    Attributes
    ----------
    api_key : str
        OpenAI API key used for authentication.
    model_url : str
        The WebSocket URL of the OpenAI Realtime API model.
    goal : str
        The assistant's instructions or goal.
    voice : str
        The voice model to use for audio output.
    tools : List[BaseTool]
        A list of tools that the agent can use.
    temperature : float
        The sampling temperature for response generation.
    modalities : List[str]
        The modes of input/output, e.g., ["text", "audio"].
    input_audio_format : str
        The format of the input audio.
    output_audio_format : str
        The format of the output audio.
    input_audio_transcription : Optional[Dict[str, Any]]
        Configuration for input audio transcription.
    turn_detection : Optional[Dict[str, Any]]
        Configuration for turn detection.
    tool_choice : str
        How the agent chooses tools, e.g., "auto".
    max_response_output_tokens : Optional[int]
        The maximum number of tokens in the response.
    """

    def __init__(
        self,
        api_key: str,
        model_url: str,
        goal: str,
        voice: str = "shimmer",
        tools: Optional[List[BaseTool]] = None,
        temperature: float = 0.7,
        modalities: Optional[List[str]] = None,
        input_audio_format: str = "pcm16",
        output_audio_format: str = "pcm16",
        input_audio_transcription: Optional[Dict[str, Any]] = None,
        turn_detection: Optional[Dict[str, Any]] = None,
        tool_choice: str = "auto",
        max_response_output_tokens: Optional[int] = None,
    ):
        self.api_key = api_key
        self.model_url = model_url
        self.goal = goal
        self.tools = tools if tools is not None else []
        self.voice = voice
        self.temperature = temperature
        self.modalities = modalities if modalities is not None else ["text", "audio"]
        self.input_audio_format = input_audio_format
        self.output_audio_format = output_audio_format
        self.input_audio_transcription = input_audio_transcription
        self.turn_detection = turn_detection
        self.tool_choice = tool_choice
        self.max_response_output_tokens = max_response_output_tokens

        self.tools_by_name = {tool.name: tool for tool in self.tools}
        self._tool_call_queue: asyncio.Queue = asyncio.Queue()

        tool_names = ", ".join([tool.name for tool in self.tools])
        logging.info(
            f"\nInitializing VoiceAgent\n"
            f"--------------------------\n"
            f"name: {self.__class__.__name__}\n"
            f"tools: {tool_names}\n"
            f"model_url: {self.model_url}\n"
            f"voice: {self.voice}\n"
        )

    async def close_connection(self) -> None:
        """
        Allows external code to signal that the agent should close its connection
        to the OpenAI Realtime API at the next available opportunity.
        """
        logging.info("VoiceAgent.close_connection() called. Will stop main loop soon.")
        self._should_close = True

    async def connect(
        self,
        input_audio_stream: AsyncIterator[str],
        handle_output_event: Callable[[str], Coroutine[Any, Any, None]],
    ) -> None:
        """
        Connects to the OpenAI Realtime API WebSocket and handles communication.

        Parameters
        ----------
        input_audio_stream : AsyncIterator[str]
            Asynchronous iterator of input audio events to send to the model.
        handle_output_event : Callable[[str], Coroutine[Any, Any, None]]
            Callback to handle output events from the model.
        """

        self._should_close = False

        async with websocket_connection(
            model_url=self.model_url,
            api_key=self.api_key,
        ) as (send_event, receive_event_stream):
            # Send initial session update with tools and instructions
            tool_definitions = [
                {
                    "type": "function",
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {"type": "object", "properties": tool.args},
                }
                for tool in self.tools_by_name.values()
            ]

            session_config = {
                "instructions": self.goal,
                "voice": self.voice,
                "temperature": self.temperature,
                "tools": tool_definitions,
                "tool_choice": self.tool_choice,
                "input_audio_transcription": (
                    self.input_audio_transcription
                    if self.input_audio_transcription
                    else None
                ),
            }
            if self.modalities:
                session_config["modalities"] = self.modalities
            if self.input_audio_format != "pcm16":
                session_config["input_audio_format"] = self.input_audio_format
            if self.output_audio_format != "pcm16":
                session_config["output_audio_format"] = self.output_audio_format
            if self.turn_detection:
                session_config["turn_detection"] = self.turn_detection
            if self.max_response_output_tokens is not None:
                session_config["max_response_output_tokens"] = (
                    self.max_response_output_tokens
                )

            await send_event(
                {
                    "type": SESSION_UPDATE,
                    "session": session_config,
                }
            )

            # Merge input streams (audio, model output, tool outputs) into one
            async for stream_name, event_data in self._merge_streams(
                input_audio=input_audio_stream,
                model_output=receive_event_stream,
                tool_outputs=self._tool_output_stream(),
            ):
                # --------------------------------------------------------------------------------
                # Parse event data from the other streams
                if isinstance(event_data, str):
                    try:
                        event = json.loads(event_data)
                    except json.JSONDecodeError:
                        logging.error(f"Error decoding JSON: {event_data}")
                        continue
                else:
                    event = event_data

                # Audio input stream => forward to OpenAI Realtime
                if stream_name == "input_audio":
                    await send_event(event)

                # Tool outputs => forward them, then trigger a new model response
                elif stream_name == "tool_outputs":
                    # If the tool_outputs stream hands us a "call_end_signal", raise CallEndException
                    # so that we can end the call in the parent function.
                    logging.info("Recieved CALL_END from stream_name: tool_outputs")
                    if event.get("type") == CALL_END:
                        await self._handle_model_output_event(
                            event, handle_output_event
                        )
                        self._should_close = True
                    else:
                        await send_event(event)
                        await send_event({"type": RESPONSE_CREATE, "response": {}})

                # Model output => handle or forward it
                elif stream_name == "model_output":
                    if event.get("type") == INPUT_AUDIO_BUFFER_SPEECH_STARTED:
                        # If user begins talking again, cancel
                        await send_event({"type": RESPONSE_CANCEL})
                    await self._handle_model_output_event(event, handle_output_event)

                # Check after processing the event, in case we set it inside the handling
                if self._should_close:
                    logging.info("VoiceAgent.connect: Closing after event handling.")
                    break

    async def _handle_model_output_event(
        self,
        event: Dict[str, Any],
        handle_output_event: Callable[[str], Coroutine[Any, Any, None]],
    ) -> None:
        """
        Processes events received from the model.
        Parameters
        ----------
        event : Dict[str, Any]
            The event data received from the model.
        handle_output_event : Callable[[str], Coroutine[Any, Any, None]]
            Callback to handle output events.
        """
        event_type = event.get("type")
        if event_type == RESPONSE_AUDIO_DELTA:
            # Audio to be played to the user
            await handle_output_event(json.dumps(event))
        elif event_type == INPUT_AUDIO_BUFFER_SPEECH_STARTED:
            await handle_output_event(json.dumps(event))
        elif event_type == CALL_END:
            logging.info("Ending the call. Recieved CALL_END event.")
            await handle_output_event(json.dumps(event))
        elif event_type == ERROR:
            logging.error(f"Error event received: {event}")
        elif event_type == RESPONSE_FUNCTION_CALL_ARGUMENTS_DONE:
            await self._add_tool_call(event)
        elif event_type == RESPONSE_AUDIO_TRANSCRIPT_DONE:
            logging.info(f"Assistant transcript: {event.get('transcript', '')}")
        elif event_type == INPUT_AUDIO_TRANSCRIPTION_COMPLETED:
            logging.info(f"User transcript: {event.get('transcript', '')}")
        elif event_type in EVENTS_TO_IGNORE:
            pass
        else:
            logging.warning(f"Unhandled event type: {event_type}")

    async def _add_tool_call(self, tool_call_data: Dict[str, Any]) -> None:
        """
        Adds a tool call to our queue to be executed asynchronously.

        Parameters
        ----------
        tool_call_data : Dict[str, Any]
            The data related to the tool call.
        """
        await self._tool_call_queue.put(tool_call_data)

    async def _execute_tool_call(
        self, tool_call_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes a tool call and returns a conversation item event with the tool's result.
        Parameters
        ----------
        tool_call_data : Dict[str, Any]
            The data related to the tool call.

        Returns
        -------
        Dict[str, Any]
            The event containing the tool execution result.
        """
        tool = self.tools_by_name.get(tool_call_data["name"])
        if tool is None:
            raise ValueError(
                f"Tool '{tool_call_data['name']}' not found. Available tools: {list(self.tools_by_name.keys())}"
            )

        # Parse arguments
        try:
            args = json.loads(tool_call_data["arguments"])
        except json.JSONDecodeError:
            raise ValueError(
                f"Failed to parse arguments '{tool_call_data['arguments']}'. Must be valid JSON."
            )

        result = await tool.ainvoke(args)
        try:
            result_str = json.dumps(result)
        except TypeError:
            result_str = str(result)

        return {
            "type": CONVERSATION_ITEM_CREATE,
            "item": {
                "id": tool_call_data["call_id"],
                "call_id": tool_call_data["call_id"],
                "type": "function_call_output",
                "output": result_str,
            },
        }

    async def _tool_output_stream(self) -> AsyncIterator[Dict[str, Any]]:
        """
        Retrieves tool calls from the queue, executes them, and yields their outputs.
        Yields
        ------
        Dict[str, Any]
            Tool execution output data.
        """
        while True:
            tool_call_data = await self._tool_call_queue.get()
            try:
                result_event = await self._execute_tool_call(tool_call_data)
                yield result_event
            except CallEndException as e:
                # Instead of re-raising, we send a special "call_end_signal"
                logging.error("CallEndException recieved inside _tool_output_stream")
                yield {
                    "type": CALL_END,
                    "item": {},
                }
                break  # terminate this generator
            except Exception as e:
                # Any other error => yield error message
                yield {
                    "type": CONVERSATION_ITEM_CREATE,
                    "item": {
                        "id": tool_call_data["call_id"],
                        "call_id": tool_call_data["call_id"],
                        "type": "function_call_output",
                        "output": f"Error: {str(e)}",
                    },
                }

    async def ainvoke(
        self,
        input_audio_stream: AsyncIterator[str],
        handle_output_event: Callable[[str], Coroutine[Any, Any, None]],
    ) -> None:
        """
        Asynchronously invokes the agent with the given input and output handlers.

        Parameters
        ----------
        input_audio_stream : AsyncIterator[str]
            The input audio stream to be processed by the agent.
            For example:
            ```
            event = {
                "type": "input_audio_buffer.append",
                "audio": base64_chunk
            }
            ```
        handle_output_event : Callable[[str], Coroutine[Any, Any, None]]
            The callback function to handle output events.
            This could be a websocket send method to emit events to client.
        """
        await self.connect(input_audio_stream, handle_output_event)

    async def _merge_streams(
        self, **streams: AsyncIterator[Any]
    ) -> AsyncIterator[Tuple[str, Any]]:
        """
        Merges multiple asynchronous iterators into a single iterator.

        Parameters
        ----------
        **streams : AsyncIterator[Any]
            Named asynchronous iterators to be merged.

        Yields
        ------
        Tuple[str, Any]
            A tuple containing the stream name and the data from the stream.
        """
        queue: asyncio.Queue = asyncio.Queue()

        async def read_stream(name: str, stream: AsyncIterator[Any]) -> None:
            async for data in stream:
                await queue.put((name, data))
            await queue.put((name, None))  # Mark that this stream is done

        tasks = [
            asyncio.create_task(read_stream(name, stream))
            for name, stream in streams.items()
        ]
        active_streams = set(streams.keys())

        try:
            while active_streams:
                stream_name, data = await queue.get()
                if data is None:
                    # one stream is finished
                    active_streams.remove(stream_name)
                else:
                    yield stream_name, data
                # If we've been flagged for closure mid-merge, break
                if self._should_close:
                    break
        finally:
            # Cleanup tasks
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
