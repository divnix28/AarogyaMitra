import pytest
from app.hrrs.thresholds import determine_action, HRRSAction
from app.hrrs.calculator import HRRSCalculator
from app.hrrs.factors import HRRSFactors
from app.safety.schemas import SafetyValidationResponse, RiskLevel

def test_determine_action_thresholds():
    # Tests the exact boundary cutoffs defined in the project requirements
    assert determine_action(100.0) == HRRSAction.ANSWER
    assert determine_action(90.0) == HRRSAction.ANSWER
    assert determine_action(89.9) == HRRSAction.ANSWER_PREVENTIVE
    assert determine_action(75.0) == HRRSAction.ANSWER_PREVENTIVE
    assert determine_action(74.9) == HRRSAction.ASK_MORE
    assert determine_action(60.0) == HRRSAction.ASK_MORE
    assert determine_action(59.9) == HRRSAction.ASHA_REFERRAL
    assert determine_action(40.0) == HRRSAction.ASHA_REFERRAL
    assert determine_action(39.9) == HRRSAction.ESCALATE
    assert determine_action(0.0) == HRRSAction.ESCALATE

def test_hrrs_calculator_safe_high_score():
    calculator = HRRSCalculator()
    
    # Simulating a perfect 100/100 scenario
    factors = HRRSFactors(
        guideline_match=100.0,
        context_completeness=100.0,
        safety_validation=100.0,
        intent_confidence=100.0,
        retrieval_quality=100.0
    )
    safety_response = SafetyValidationResponse(
        is_safe=True, 
        risk_level=RiskLevel.SAFE, 
        reason="Clear"
    )
    
    result = calculator.calculate(factors, safety_response)
    
    assert result.score == 100.0
    assert result.action == HRRSAction.ANSWER
    assert len(result.reason_codes) == 0

def test_hrrs_calculator_safety_override():
    calculator = HRRSCalculator()
    
    # Simulating high technical scores (e.g., highly confident retrieval of emergency advice)
    factors = HRRSFactors(
        guideline_match=90.0,
        context_completeness=90.0,
        safety_validation=90.0,
        intent_confidence=90.0,
        retrieval_quality=90.0
    )
    # The safety gate correctly flags it as an emergency
    safety_response = SafetyValidationResponse(
        is_safe=False, 
        risk_level=RiskLevel.EMERGENCY, 
        reason="Emergency keyword detected"
    )
    
    result = calculator.calculate(factors, safety_response)
    
    # The system must override the high score, cap it, and escalate
    assert result.score <= 39.0
    assert result.action == HRRSAction.ESCALATE
    assert "SAFETY_OVERRIDE_EMERGENCY" in result.reason_codes