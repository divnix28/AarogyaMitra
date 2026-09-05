from pydantic import BaseModel
from typing import Optional, List

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
    sources: Optional[List[dict]] = []  # Explicitly accepts Member 4's data