EMERGENCY_KEYWORDS = [
    "heart attack", "suicide", "bleeding heavily", "unconscious", 
    "cannot breathe", "poison", "overdose", "stroke", "emergency"
]

HIGH_RISK_INTENTS = [
    "prescribe_medication", 
    "diagnose_symptom", 
    "treatment_recommendation"
]

def contains_emergency_indicators(message: str) -> bool:
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in EMERGENCY_KEYWORDS)

def is_high_risk_intent(intent: str) -> bool:
    return intent in HIGH_RISK_INTENTS