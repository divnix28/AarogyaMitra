from datetime import datetime, timedelta, timezone
from pydantic import BaseModel

class RetentionSchedule(BaseModel):
    topic: str
    next_review_date: datetime

def schedule_next_review(topic: str, current_interval_days: int) -> RetentionSchedule:
    schedule_progression = {0: 1, 1: 3, 3: 7, 7: 30}
    
    next_interval = schedule_progression.get(current_interval_days, 30)
    # Replaced utcnow() with now(timezone.utc)
    next_date = datetime.now(timezone.utc) + timedelta(days=next_interval)
    
    return RetentionSchedule(
        topic=topic,
        next_review_date=next_date
    )