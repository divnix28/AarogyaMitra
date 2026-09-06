from datetime import datetime, timezone
from typing import Union

from pydantic import BaseModel
from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_chat_pipeline

router = APIRouter()


class LegacyChatRequest(BaseModel):
    sender: str | None = None
    channel: str = "web"
    user_id: str | None = None
    message: str
    language: str = "en"
    timestamp: str | None = None


def _normalize_chat_request(payload: dict) -> ChatRequest:
    normalized = dict(payload)
    if "sender" in normalized and "user_id" not in normalized:
        normalized["user_id"] = normalized["sender"]
    if "user_id" in normalized and normalized["user_id"] is not None and "sender" not in normalized:
        normalized["sender"] = normalized["user_id"]
    if "channel" not in normalized:
        normalized["channel"] = "web"
    if "timestamp" not in normalized or not normalized["timestamp"]:
        normalized["timestamp"] = datetime.now(timezone.utc).isoformat()
    if "language" not in normalized:
        normalized["language"] = "en"
    return ChatRequest(**normalized)


@router.post("/message", response_model=ChatResponse)
async def process_chat_message(request: Union[ChatRequest, LegacyChatRequest]):
    if isinstance(request, LegacyChatRequest):
        normalized_request = _normalize_chat_request(request.model_dump())
    else:
        normalized_request = request

    pipeline_result = process_chat_pipeline(normalized_request)
    return ChatResponse(**pipeline_result)