from pydantic import BaseModel

# Weights must sum exactly to 1.0 (100%)
WEIGHTS = {
    "guideline_match": 0.30,
    "context_completeness": 0.20,
    "safety_validation": 0.20,
    "intent_confidence": 0.15,
    "retrieval_quality": 0.15
}

class HRRSFactors(BaseModel):
    guideline_match: float       # Scale: 0 to 100
    context_completeness: float  # Scale: 0 to 100
    safety_validation: float     # Scale: 0 to 100
    intent_confidence: float     # Scale: 0 to 100
    retrieval_quality: float     # Scale: 0 to 100