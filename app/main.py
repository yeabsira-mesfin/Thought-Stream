import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.model_adapter import generate_response
from app.security import event_id, sanitize_output, tool_allowed, validate_prompt


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-security-lab")

app = FastAPI(
    title="AI Security Testing Lab",
    version="1.0.0",
    description="Defensive controls for AI-enabled applications.",
)


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    requested_tool: str | None = Field(default=None, max_length=64)


class ChatResponse(BaseModel):
    response: str
    security_event_id: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    validation = validate_prompt(request.prompt)
    request_id = event_id(request.prompt)

    if not validation.allowed:
        logger.warning("security_event id=%s decision=blocked reason=%s", request_id, validation.reason)
        raise HTTPException(status_code=400, detail=validation.reason)

    if not tool_allowed(request.requested_tool):
        logger.warning("security_event id=%s decision=blocked reason=tool_not_allowed", request_id)
        raise HTTPException(status_code=403, detail="requested tool is not allowed")

    output = generate_response(validation.sanitized_text, request.requested_tool)
    safe_output = sanitize_output(output)

    logger.info("security_event id=%s decision=allowed", request_id)
    return ChatResponse(response=safe_output, security_event_id=request_id)
