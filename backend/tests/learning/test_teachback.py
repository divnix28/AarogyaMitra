from app.learning.teachback import evaluate_understanding, UnderstandingLevel

def test_evaluate_understanding_needs_reteaching():
    # Tests the fallback logic for short, ambiguous answers
    result = evaluate_understanding("I forgot")
    assert result.level == UnderstandingLevel.NEEDS_RETEACHING
    assert "tell me a bit more" in result.feedback_message

def test_evaluate_understanding_understood():
    # Tests a sufficiently long explanation
    result = evaluate_understanding("Antibiotics only kill bacteria, not viruses.")
    assert result.level == UnderstandingLevel.UNDERSTOOD
    assert result.feedback_message == "Great, you've got it!"