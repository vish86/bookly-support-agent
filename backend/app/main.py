from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .agent import simple_agent_turn
from .schemas import ChatRequest, ChatResponse, ChatMessage


app = FastAPI(title="Bookly Support Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    if not request.messages:
        raise HTTPException(status_code=400, detail="At least one message is required.")

    last_message = request.messages[-1]
    if last_message.role != "user":
        raise HTTPException(
            status_code=400,
            detail="Last message in the conversation must be from the user.",
        )

    assistant_message, metadata = simple_agent_turn(request.messages)

    conversation_id = request.conversation_id or "local-session"

    return ChatResponse(
        conversation_id=conversation_id,
        message=assistant_message,
        action_metadata=metadata,
    )


def create_app() -> FastAPI:
    """
    Factory for creating the FastAPI app (useful for testing).
    """
    return app

