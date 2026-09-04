from pydantic import BaseModel
from typing import List
from .factors import HRRSFactors, WEIGHTS
from .thresholds import HRRSAction, determine_action
from app.safety.schemas import SafetyValidationResponse, RiskLevel

class HRRSResult(BaseModel):
    score: float
    factors: HRRSFactors
    action: HRRSAction
    reason_codes: List[str]

class HRRSCalculator:
    def calculate(self, factors: HRRSFactors, safety_response: SafetyValidationResponse) -> HRRSResult:
        # Calculate the deterministic base score
        score = (
            factors.guideline_match * WEIGHTS["guideline_match"] +
            factors.context_completeness * WEIGHTS["context_completeness"] +
            factors.safety_validation * WEIGHTS["safety_validation"] +
            factors.intent_confidence * WEIGHTS["intent_confidence"] +
            factors.retrieval_quality * WEIGHTS["retrieval_quality"]
        )
        
        action = determine_action(score)
        reason_codes = []

        # Strict Safety Override: Safety gates bypass any high mathematical score
        if not safety_response.is_safe:
            action = HRRSAction.ESCALATE
            reason_codes.append(f"SAFETY_OVERRIDE_{safety_response.risk_level.value}")
            score = min(score, 39.0)  # Conceptually cap score to reflect escalation

        return HRRSResult(
            score=round(score, 2),
            factors=factors,
            action=action,
            reason_codes=reason_codes
        )