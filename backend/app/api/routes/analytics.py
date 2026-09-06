from fastapi import APIRouter, Depends
from app.api.deps import require_role

router = APIRouter()

@router.get("/trends")
def get_symptom_trends(current_user: dict = Depends(require_role("ASHA"))):
    """
    Returns aggregated community symptom data. 
    Protected route: Only accessible with a valid ASHA JWT token.
    """
    return {
        "status": "success",
        "region": "Kothri Kalan",
        "timeframe": "last_7_days",
        "data": [
            {"symptom": "fever", "occurrences": 42, "trend": "up", "risk": "moderate"},
            {"symptom": "fatigue", "occurrences": 28, "trend": "stable", "risk": "low"},
            {"symptom": "chest pain", "occurrences": 2, "trend": "down", "risk": "critical"}
        ]
    }

