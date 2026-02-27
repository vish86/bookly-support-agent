from __future__ import annotations

import json
from typing import Any, Literal, TypedDict

from .llm_client import chat_completion
from .schemas import ActionMetadata, ChatMessage
from .tools import (
    evaluate_refund_eligibility,
    get_policy_answer,
    list_recent_orders,
    lookup_order,
)


class ActionObject(TypedDict, total=False):
    action: Literal["ask_clarification", "call_tool", "answer"]
    clarifying_question: str
    tool_name: str
    tool_args: dict[str, Any]
    answer_text: str


def build_system_prompt() -> str:
    """
    System prompt encoding the Bookly domain, tools, and required action schema.
    """
    return (
        "You are Bookly's formal and concise customer support agent. "
        "You assist customers with order status, returns and refunds, and general "
        "policy questions (shipping, refunds, password reset). "
        "You must ALWAYS respond with a single valid JSON object describing your "
        "next action, without any additional commentary.\n\n"
        "Action schema:\n"
        "{\n"
        '  \"action\": \"ask_clarification\" | \"call_tool\" | \"answer\",\n'
        '  \"clarifying_question\": string (optional),\n'
        '  \"tool_name\": \"lookup_order\" | \"list_recent_orders\" | '
        '\"evaluate_refund_eligibility\" | \"get_policy_answer\" (optional),\n'
        '  \"tool_args\": object with the exact arguments for the tool (optional),\n'
        '  \"answer_text\": string (optional, final user-facing answer)\n'
        "}\n\n"
        "Tools:\n"
        "- lookup_order(order_id, email_or_last_name): use when the user provides or "
        "can reasonably be asked for a specific order id; verifies that the order "
        "belongs to the customer.\n"
        "- list_recent_orders(email): use when the user mentions \"my last order\" or "
        "similar and only provides an email.\n"
        "- evaluate_refund_eligibility(order_id, reason): use when the user clearly "
        "wants a return or refund and you know which order they mean.\n"
        "- get_policy_answer(topic): use for general policy questions about "
        "\"shipping\", \"returns\", \"refunds\", or \"password_reset\".\n\n"
        "Guidelines:\n"
        "- Ask a clarifying question when you are missing essential information, "
        "such as order id or email.\n"
        "- Never invent order ids or shipment events; use tools for order data.\n"
        "- For out-of-scope questions, set action=\"answer\" and answer_text to a "
        "polite explanation that the question is outside Bookly's scope.\n"
        "Return ONLY the JSON object, nothing else."
    )


def _build_decision_messages(messages: list[ChatMessage]) -> list[dict[str, Any]]:
    """
    Convert typed messages into the dict format expected by the OpenAI client for
    the decision step, prefixing a system message with behavior and schema.
    """
    system_message = {"role": "system", "content": build_system_prompt()}
    converted = [system_message]
    for m in messages:
        converted.append({"role": m.role, "content": m.content})
    return converted


def _parse_action_object(raw: str) -> ActionObject:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model did not return valid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("Action object must be a JSON object.")

    action = data.get("action")

    # Happy path: action explicitly matches the supported verbs.
    if action in {"ask_clarification", "call_tool", "answer"}:
        return data  # type: ignore[return-value]

    # Model sometimes returns the tool name as the action, e.g.:
    # { "action": "lookup_order", "order_id": "...", "email_or_last_name": "..." }
    tool_like_actions = {
        "lookup_order",
        "list_recent_orders",
        "evaluate_refund_eligibility",
        "get_policy_answer",
    }
    if isinstance(action, str) and action in tool_like_actions:
        tool_args = data.get("tool_args")
        if not isinstance(tool_args, dict):
            # Treat all other top-level fields as arguments.
            tool_args = {
                k: v
                for k, v in data.items()
                if k not in {"action", "tool_name", "tool_args", "answer_text"}
            }
        return {
            "action": "call_tool",
            "tool_name": action,
            "tool_args": tool_args,
        }

    raise ValueError(
        "Action field must be one of ask_clarification, call_tool, answer, "
        "or a known tool name."
    )


def _decide_next_action(messages: list[ChatMessage]) -> ActionObject:
    """
    Call the LLM to obtain an action object, with a single retry on schema failure.
    """
    decision_messages = _build_decision_messages(messages)
    raw = chat_completion(decision_messages, temperature=0.1)

    try:
        return _parse_action_object(raw)
    except ValueError:
        retry_system = {
            "role": "system",
            "content": (
                build_system_prompt()
                + "\nThe previous response was invalid. Return ONLY a valid JSON object."
            ),
        }
        retry_messages = [retry_system] + decision_messages[1:]
        raw_retry = chat_completion(retry_messages, temperature=0.0)

        try:
            return _parse_action_object(raw_retry)
        except ValueError:
            # If the model still does not follow the schema, fall back to treating
            # its response as a direct answer to the user.
            fallback_text = raw_retry or raw or (
                "I could not reliably interpret your request, but here is my best attempt "
                "to respond based on the information provided."
            )
            return {
                "action": "answer",
                "answer_text": fallback_text,
            }


def _call_tool(tool_name: str, tool_args: dict[str, Any]) -> dict[str, Any]:
    if tool_name == "lookup_order":
        return lookup_order(
            order_id=str(tool_args.get("order_id", "")),
            email_or_last_name=str(tool_args.get("email_or_last_name", "")),
        )
    if tool_name == "list_recent_orders":
        return {
            "orders": list_recent_orders(email=str(tool_args.get("email", ""))),
        }
    if tool_name == "evaluate_refund_eligibility":
        return evaluate_refund_eligibility(
            order_id=str(tool_args.get("order_id", "")),
            reason=str(tool_args.get("reason", "")),
        )
    if tool_name == "get_policy_answer":
        topic = str(tool_args.get("topic", ""))
        policy = get_policy_answer(topic)
        return {"policy": policy, "topic": topic}

    raise ValueError(f"Unknown tool: {tool_name}")


def _build_answer_from_tool(
    last_user_message: ChatMessage,
    tool_name: str,
    tool_result: dict[str, Any],
) -> str:
    """
    Use the LLM to turn a tool result into a concise, user-facing answer.
    """
    system = {
        "role": "system",
        "content": (
            "You are Bookly's formal and concise support agent. "
            "Given the user's question and the structured tool result, "
            "write a short, professional answer. Do not mention internal tools."
        ),
    }
    user = {
        "role": "user",
        "content": (
            f"User question: {last_user_message.content}\n\n"
            f"Tool used: {tool_name}\n"
            f"Structured tool result (JSON): {json.dumps(tool_result, ensure_ascii=False)}\n\n"
            "Write a concise response to the user summarizing the relevant details."
        ),
    }
    return chat_completion([system, user], temperature=0.2)


def agent_turn(messages: list[ChatMessage]) -> tuple[ChatMessage, ActionMetadata]:
    """
    Full agent turn implementation that:
    - Asks clarifying questions when required.
    - Calls tools backed by synthetic Bookly data when appropriate.
    - Produces a formal, concise assistant message and structured metadata.
    """
    action_obj = _decide_next_action(messages)
    action = action_obj.get("action", "answer")
    last_user_message = messages[-1]

    if action == "ask_clarification":
        question = action_obj.get("clarifying_question") or (
            "Could you please provide a bit more detail so I can help you accurately?"
        )
        assistant_message = ChatMessage(role="assistant", content=question)
        metadata = ActionMetadata(
            action="ask_clarification",
            tool_name=None,
            tool_args=None,
            is_clarifying_question=True,
        )
        return assistant_message, metadata

    if action == "answer":
        answer_text = action_obj.get("answer_text") or (
            "Here is the information I can provide based on your request."
        )
        assistant_message = ChatMessage(role="assistant", content=answer_text)
        metadata = ActionMetadata(
            action="answer",
            tool_name=None,
            tool_args=None,
            is_clarifying_question=False,
        )
        return assistant_message, metadata

    # action == "call_tool"
    tool_name = action_obj.get("tool_name")
    tool_args = action_obj.get("tool_args") or {}
    if not tool_name:
        # Fallback: treat as clarification request if the model forgot to set tool_name.
        assistant_message = ChatMessage(
            role="assistant",
            content=(
                "I need a bit more information before I can look up your request. "
                "Could you clarify the order id or email associated with your account?"
            ),
        )
        metadata = ActionMetadata(
            action="ask_clarification",
            tool_name=None,
            tool_args=None,
            is_clarifying_question=True,
        )
        return assistant_message, metadata

    tool_result = _call_tool(tool_name, tool_args)
    final_text = _build_answer_from_tool(last_user_message, tool_name, tool_result)

    assistant_message = ChatMessage(role="assistant", content=final_text)
    metadata = ActionMetadata(
        action="call_tool",
        tool_name=tool_name,
        tool_args=tool_args,
        is_clarifying_question=False,
    )
    return assistant_message, metadata


