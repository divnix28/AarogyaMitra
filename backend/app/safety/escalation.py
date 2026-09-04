from .schemas import RiskLevel

ESCALATION_MESSAGES = {
    RiskLevel.EMERGENCY: "This sounds like a medical emergency. Please contact your local emergency services or visit the nearest hospital immediately. I cannot provide emergency medical assistance.",
    RiskLevel.HIGH_RISK: "I am an AI health assistant and cannot diagnose conditions or prescribe medications. Please consult a qualified healthcare professional for this issue.",
    RiskLevel.INSUFFICIENT_CONTEXT: "I don't have enough information to safely answer this. Could you please provide more details, or consult a healthcare worker?"
}

def get_escalation_message(risk_level: RiskLevel) -> str:
    return ESCALATION_MESSAGES.get(risk_level, "")