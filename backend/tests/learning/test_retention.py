from datetime import datetime, timedelta, timezone
from app.learning.retention import schedule_next_review

def test_schedule_initial_review():
    result = schedule_next_review("Diabetes", 0)
    # Replaced utcnow() with now(timezone.utc)
    expected_date = datetime.now(timezone.utc) + timedelta(days=1)
    
    assert result.topic == "Diabetes"
    assert result.next_review_date.date() == expected_date.date()

def test_schedule_advanced_review():
    result = schedule_next_review("Antibiotics", 7)
    # Replaced utcnow() with now(timezone.utc)
    expected_date = datetime.now(timezone.utc) + timedelta(days=30)
    
    assert result.next_review_date.date() == expected_date.date()