from typing import Any

from .llm_client import chat_completion
from .schemas import ActionMetadata, ChatMessage


def build_system_prompt() -> str:
    """
    System prompt encoding the Bookly domain and agent behavior at a high level.
    Detailed tool instructions will be added when tools are implemented.
    """
    return (
        "You are Bookly's formal and concise customer support agent. "
        "You assist users with order status, returns and refunds, and general policy "
        "questions about shipping and password reset. "
        "Respond clearly and professionally in a few sentences."
    )


def build_prompt_messages(messages: list[ChatMessage]) -> list[dict[str, Any]]:
    """
    Convert typed messages into the dict format expected by the OpenAI client,
    prefixing a system message with high-level behavior instructions.
    """
    system_message = {"role": "system", "content": build_system_prompt()}
    converted = [system_message]
    for m in messages:
        converted.append({"role": m.role, "content": m.content})
    return converted


def simple_agent_turn(messages: list[ChatMessage]) -> tuple[ChatMessage, ActionMetadata]:
    """
    Minimal agent turn implementation for the prototype backend skeleton.

    For Task 2, we delegate the full response to the LLM without explicit tools.
    Later tasks will replace this with structured action objects and tool calls.
    """
    prompt_messages = build_prompt_messages(messages)
    content = chat_completion(prompt_messages)

    assistant_message = ChatMessage(role="assistant", content=content)
    metadata = ActionMetadata(
        action="answer",
        tool_name=None,
        tool_args=None,
        is_clarifying_question=False,
    )
    return assistant_message, metadata

