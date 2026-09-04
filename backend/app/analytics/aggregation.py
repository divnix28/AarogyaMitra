from pydantic import BaseModel
from typing import List, Dict, Optional

class AnonymizedInteraction(BaseModel):
    topic: str
    symptom_mentioned: Optional[str] = None
    timestamp: str

def aggregate_daily_topics(interactions: List[AnonymizedInteraction]) -> Dict[str, int]:
    # Strictly counts topics without exposing any Personally Identifiable Information (PII)
    topic_counts = {}
    for interaction in interactions:
        topic_counts[interaction.topic] = topic_counts.get(interaction.topic, 0) + 1
    return topic_counts