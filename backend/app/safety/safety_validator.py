from .schemas import SafetyValidationRequest, SafetyValidationResponse, RiskLevel
from .risk_rules import contains_emergency_indicators, is_high_risk_intent
from .escalation import get_escalation_message

class SafetyValidator:
    def validate(self, request: SafetyValidationRequest) -> SafetyValidationResponse:
        if not request.user_message or not request.user_message.strip():
            return SafetyValidationResponse(
                is_safe=False,
                risk_level=RiskLevel.INSUFFICIENT_CONTEXT,
                reason="Empty or insufficient user message.",
                escalation_message=get_escalation_message(RiskLevel.INSUFFICIENT_CONTEXT)
            )

        if contains_emergency_indicators(request.user_message):
            return SafetyValidationResponse(
                is_safe=False,
                risk_level=RiskLevel.EMERGENCY,
                reason="Emergency indicators detected in user message.",
                escalation_message=get_escalation_message(RiskLevel.EMERGENCY)
            )

        if request.intent and is_high_risk_intent(request.intent):
            return SafetyValidationResponse(
                is_safe=False,
                risk_level=RiskLevel.HIGH_RISK,
                reason="High-risk medical intent detected.",
                escalation_message=get_escalation_message(RiskLevel.HIGH_RISK)
            )

        return SafetyValidationResponse(
            is_safe=True,
            risk_level=RiskLevel.SAFE,
            reason="Message passed preliminary safety checks."
        )