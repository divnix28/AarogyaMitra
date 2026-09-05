from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_chat_pipeline

router = APIRouter()

@router.post("/message", response_model=ChatResponse)
async def process_chat_message(request: ChatRequest):
    pipeline_result = process_chat_pipeline(request)
    return ChatResponse(**pipeline_result)