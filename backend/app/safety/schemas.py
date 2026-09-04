from pydantic import BaseModel
from typing import Optional
from enum import Enum

class RiskLevel(str, Enum):
    SAFE = "SAFE"
    INSUFFICIENT_CONTEXT = "INSUFFICIENT_CONTEXT"
    HIGH_RISK = "HIGH_RISK"
    EMERGENCY = "EMERGENCY"

class SafetyValidationRequest(BaseModel):
    user_message: str
    intent: Optional[str] = None
    entities: Optional[dict] = None

class SafetyValidationResponse(BaseModel):
    is_safe: bool
    risk_level: RiskLevel
    reason: str
    escalation_message: Optional[str] = None