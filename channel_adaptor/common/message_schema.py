from pydantic import BaseModel, Field
from typing import Optional
import datetime

class CommonMessage(BaseModel):
    user_id: str
    message: str  # Must match Member 1's backend ChatRequest schema
    channel: str = "whatsapp"
    message_id: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    phone_number: Optional[str] = None
    language: str = "en"
