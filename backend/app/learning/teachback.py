from pydantic import BaseModel
from enum import Enum

class UnderstandingLevel(str, Enum):
    UNDERSTOOD = "UNDERSTOOD"
    NEEDS_RETEACHING = "NEEDS_RETEACHING"
    AMBIGUOUS = "AMBIGUOUS"

class TeachBackEvaluation(BaseModel):
    level: UnderstandingLevel
    feedback_message: str

def evaluate_understanding(user_explanation: str) -> TeachBackEvaluation:
    word_count = len(user_explanation.split())
    
    if word_count < 3:
        return TeachBackEvaluation(
            level=UnderstandingLevel.NEEDS_RETEACHING,
            feedback_message="I want to make sure I explained that well. Could you tell me a bit more about how you understand it?"
        )
        
    return TeachBackEvaluation(
        level=UnderstandingLevel.UNDERSTOOD,
        feedback_message="Great, you've got it!"
    )