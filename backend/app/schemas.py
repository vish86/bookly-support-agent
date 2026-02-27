from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"] = Field(..., description="Message role.")
    content: str = Field(..., description="Message content.")


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = Field(
        default=None,
        description="Opaque client conversation identifier (optional, not persisted).",
    )
    messages: list[ChatMessage] = Field(
        ..., description="Ordered list of prior messages including the latest user message."
    )


class ActionMetadata(BaseModel):
    action: Literal["ask_clarification", "call_tool", "answer"] = Field(
        ..., description="High-level agent decision for this turn."
    )
    tool_name: Optional[str] = Field(
        default=None, description="Name of tool used, if any."
    )
    tool_args: Optional[dict[str, Any]] = Field(
        default=None, description="Arguments passed to the tool, if any."
    )
    is_clarifying_question: bool = Field(
        default=False,
        description="Whether the assistant message is primarily a clarifying question.",
    )


class ChatResponse(BaseModel):
    conversation_id: str = Field(
        ..., description="Echoed or generated conversation identifier."
    )
    message: ChatMessage = Field(..., description="Assistant message for this turn.")
    action_metadata: ActionMetadata = Field(
        ..., description="Structured metadata about agent decision making."
    )

