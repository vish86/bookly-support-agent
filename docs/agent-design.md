# Bookly Support Agent – Design

## 1. Goals and Scope

Design a formal, concise customer support agent for **Bookly**, a fictional online bookstore, that:

- Handles **order status**, **returns/refunds**, and **general policy questions**.
- Demonstrates **multi-turn conversation**, **tool usage**, and **clarifying questions**.
- Uses a **web-based chat UI** and a **Python FastAPI backend** with OpenAI GPT-4o-mini.
- Emphasizes clear design, safety, and tradeoffs over production hardening.

Assumptions:

- All data is **synthetic and in-memory** (no external services or persistence).
- Users are authenticated out-of-band; we only rely on order id + email/last name.
- Only **text chat** is supported; no voice.

## 2. High-Level Architecture

- **Frontend (support console UI)**
  - Single-page React app styled like a support console window using `shadcn/ui`.
  - Shows a conversations list (mock), main chat panel, and input area.
  - Sends user messages and local conversation history to the backend via `POST /chat`.

- **Backend (FastAPI)**
  - Exposes `POST /chat` for agent interactions and `GET /health` for readiness.
  - Implements a functional **agent orchestrator**:
    - Builds prompts for GPT-4o-mini.
    - Interprets model output as **action objects**.
    - Invokes **tools** backed by synthetic Bookly data.

- **Tools & Data**
  - Pure Python functions over in-memory data:
    - `lookup_order`, `list_recent_orders`, `evaluate_refund_eligibility`, `get_policy_answer`.
  - Synthetic data includes users, orders with varied statuses, and policy text.

Data flow (single turn):

1. Frontend sends `{conversation, latest_user_message}` to `POST /chat`.
2. Backend calls GPT-4o-mini with system prompt, tools description, and conversation context.
3. Model returns an **action object**: ask for clarification, call a tool, or answer directly.
4. If a tool is called, backend invokes it, then calls the model again to generate the final reply.
5. Backend returns the reply + metadata; frontend updates the chat view.

## 3. Conversation & Decision Design

### Intents and Flows

- **Order status**
  - Recognize questions like “Where is my order?” or “Track order 1234”.
  - If identifiers missing, **ask clarifying questions** (order id and email/last name).
  - Use `lookup_order` and return status, expected delivery, and tracking (if available).
  - Handle: order not found, already delivered, delayed shipment.

- **Returns/refunds**
  - Recognize requests like “I want to return my book” or “Refund order 5678”.
  - Clarify which item (if multiple), reason, and condition.
  - Call `evaluate_refund_eligibility` and:
    - If eligible: confirm and explain refund expectations.
    - If ineligible: explain why and suggest alternatives.

- **General policy Q&A**
  - Questions about shipping times, international shipping, refund windows, password reset.
  - Use `get_policy_answer` to avoid hallucinating unsupported policies.

### Decision Rules

- **Answer directly** when:
  - The question is clearly about high-level policy (e.g. “What is your refund policy?”).
  - No specific order lookup or refund computation is required.
- **Ask a clarifying question** when:
  - The user refers to “my order” without an order id or identifying email/last name.
  - The requested action is ambiguous (multiple possible orders/items) or the information conflicts.
- **Call a tool** when:
  - The user provides (or has provided in previous turns) enough identifiers for a lookup.
  - A concrete order status, refund eligibility decision, or policy snippet is needed.

### Action Object Schema

The model is instructed to always produce a JSON **action object**:

```json
{
  "action": "ask_clarification" | "call_tool" | "answer",
  "clarifying_question": "string (optional)",
  "tool_name": "lookup_order | list_recent_orders | evaluate_refund_eligibility | get_policy_answer (optional)",
  "tool_args": { "key": "value" } ,
  "answer_text": "string (optional, final user-facing answer)"
}
```

Behavior:

- `ask_clarification`: Backend returns `clarifying_question` to the user; no tools are called.
- `call_tool`: Backend validates `tool_name` and `tool_args`, calls the tool, then calls the model again with tool results to obtain `answer_text`.
- `answer`: Backend sends `answer_text` directly without calling tools.

The backend validates this object; on invalid JSON or schema mismatch, it retries once with a stricter instruction.

If the model still fails to follow the schema, the backend falls back to treating the raw model text as a direct `answer_text` to avoid surfacing errors to the user.

## 4. Hallucination & Safety Controls

## 4. Hallucination & Safety Controls

- **Scoped knowledge**:
  - System prompt describes Booklyʼs domain, tools, and synthetic policies explicitly.
  - The agent is instructed to say **“I donʼt know”** when information is outside this scope.

- **Tool-first for sensitive data**:
  - Order details must come **only** from tools, never from the modelʼs speculation.
  - If a tool returns “not found” or ambiguity, the agent must either:
    - Ask the user for more information, or
    - Clearly state that the order cannot be located.

- **Output validation**:
  - Backend enforces the action object schema and rejects malformed actions.
  - Unknown tools or arguments are treated as errors; the agent is asked to correct itself.

- **Style and tone**:
  - Responses are formal, concise, and helpful.
  - No jokes, emojis, or unnecessary small talk.

## 5. Example System Prompt

A representative system prompt (abridged for brevity):

> “You are Booklyʼs formal and concise customer support agent. You assist customers  
> with order status, returns and refunds, and general policy questions (shipping, refunds,  
> password reset). You must always respond with a single valid JSON object describing  
> your next action, following this schema:  
> `{ "action": "ask_clarification" | "call_tool" | "answer", "clarifying_question": string?, "tool_name": "lookup_order" | "list_recent_orders" | "evaluate_refund_eligibility" | "get_policy_answer"?, "tool_args": object?, "answer_text": string? }`.  
> Use tools for concrete order and refund details, never invent order ids or shipment events,  
> and say you do not know when questions fall outside Booklyʼs scope.”

This system prompt is combined with the conversation history and (when needed) structured tool results to drive each turn.

## 6. Production Readiness and Tradeoffs

Tradeoffs made for the prototype:

- **In-memory synthetic data only**; integrating with real Bookly APIs would require authentication, authorization, and data contracts.
- **Single-process FastAPI app** without horizontal scaling, observability, or rate limiting.
- **Simple prompt-based action schema** instead of robust function-calling or a full tool orchestration framework.

To move toward production:

- Replace synthetic data with real services (orders, users, policies) behind stable APIs.
- Add observability (structured logging, tracing, metrics) and safety monitoring.
- Implement authentication, authorization, and rate limiting for API endpoints.
- Introduce evaluation harnesses and conversation replay to measure quality.
- Harden prompts, adopt function calling or JSON schema enforcement, and add red-team testing.

