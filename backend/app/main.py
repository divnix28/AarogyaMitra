from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import datetime
from app.database.connection import engine
from app.models.learning import Base
from app.services.chat_service import process_chat_pipeline

app = FastAPI(
    title="AarogyaMitra AI Core Backend",
    description="Central orchestration layer for the AarogyaMitra AI ecosystem.",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

class ChatRequest(BaseModel):
    channel: str
    user_id: str
    message: str
    language: str = "en"
    timestamp: str

class ChatResponse(BaseModel):
    message: str
    intent: Optional[str] = None
    confidence: Optional[float] = None
    action: str
    hrrs_score: Optional[int] = None
    sources: Optional[List[str]] = []

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}

@app.post("/api/v1/chat/message", response_model=ChatResponse)
async def process_chat_message(request: ChatRequest):
    pipeline_result = process_chat_pipeline(request)
    return ChatResponse(**pipeline_result)