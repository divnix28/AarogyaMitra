from pydantic import BaseModel
from typing import Optional

class MisconceptionResult(BaseModel):
    detected: bool
    topic: Optional[str] = None
    correction: Optional[str] = None
    trigger_teachback: bool = False

# Deterministic misconception mapping
COMMON_MISCONCEPTIONS = {
    "antibiotics cure viral fever": {
        "topic": "Antibiotics",
        "correction": "Antibiotics only kill bacteria, not viruses. They will not cure a viral fever.",
        "trigger_teachback": True
    },
    "sugar causes diabetes directly": {
        "topic": "Diabetes",
        "correction": "Eating sugar does not directly cause diabetes, though a diet high in sugar can lead to weight gain, which is a risk factor for Type 2 diabetes.",
        "trigger_teachback": True
    }
}

class MisconceptionDetector:
    def check_message(self, user_message: str) -> MisconceptionResult:
        message_lower = user_message.lower()
        
        for false_claim, data in COMMON_MISCONCEPTIONS.items():
            if false_claim in message_lower:
                return MisconceptionResult(
                    detected=True,
                    topic=data["topic"],
                    correction=data["correction"],
                    trigger_teachback=data["trigger_teachback"]
                )
                
        return MisconceptionResult(detected=False)