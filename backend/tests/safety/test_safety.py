from unittest.mock import patch
from app.safety.risk_rules import contains_emergency_indicators, is_high_risk_intent
from app.safety.safety_validator import SafetyValidator
from app.safety.schemas import SafetyValidationRequest, RiskLevel

def test_contains_emergency_indicators():
    # Verifies critical keywords trigger the safety net
    assert contains_emergency_indicators("Help, I think I'm having a heart attack!") == True
    assert contains_emergency_indicators("I took an overdose of pills.") == True
    assert contains_emergency_indicators("I just have a mild headache.") == False

def test_is_high_risk_intent():
    # Verifies restricted clinical intents are flagged
    assert is_high_risk_intent("prescribe_medication") == True
    assert is_high_risk_intent("diagnose_symptom") == True
    assert is_high_risk_intent("ask_dietary_advice") == False

@patch("app.safety.safety_validator.get_escalation_message")
def test_safety_validator_insufficient_context(mock_escalation):
    mock_escalation.return_value = "Mocked insufficient context message."
    validator = SafetyValidator()
    
    # Test empty string
    request = SafetyValidationRequest(user_message="   ", intent=None)
    response = validator.validate(request)
    
    assert response.is_safe == False
    assert response.risk_level == RiskLevel.INSUFFICIENT_CONTEXT

@patch("app.safety.safety_validator.get_escalation_message")
def test_safety_validator_emergency(mock_escalation):
    mock_escalation.return_value = "Mocked emergency escalation."
    validator = SafetyValidator()
    
    request = SafetyValidationRequest(user_message="He is unconscious.", intent="general_query")
    response = validator.validate(request)
    
    assert response.is_safe == False
    assert response.risk_level == RiskLevel.EMERGENCY
    mock_escalation.assert_called_once_with(RiskLevel.EMERGENCY)

@patch("app.safety.safety_validator.get_escalation_message")
def test_safety_validator_high_risk_intent(mock_escalation):
    mock_escalation.return_value = "Mocked high risk escalation."
    validator = SafetyValidator()
    
    request = SafetyValidationRequest(user_message="What should I take for this?", intent="treatment_recommendation")
    response = validator.validate(request)
    
    assert response.is_safe == False
    assert response.risk_level == RiskLevel.HIGH_RISK

def test_safety_validator_safe():
    validator = SafetyValidator()
    
    request = SafetyValidationRequest(user_message="How do I prevent dengue?", intent="preventive_health")
    response = validator.validate(request)
    
    assert response.is_safe == True
    assert response.risk_level == RiskLevel.SAFE