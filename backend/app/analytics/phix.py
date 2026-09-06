from typing import List, Dict
from .aggregation import AnonymizedInteraction, aggregate_daily_topics
from .symptom_trends import detect_symptom_surge

class PHIXEngine:
    def generate_early_signals(self, recent_interactions: List[AnonymizedInteraction], historical_data: Dict[str, float]) -> dict:
        daily_counts = aggregate_daily_topics(recent_interactions)
        surges = detect_symptom_surge(daily_counts, historical_data)
        
        return {
            "status": "success",
            "aggregated_counts": daily_counts,
            "detected_surges": surges,
            "disclaimer": "These are early community intelligence signals, not confirmed clinical outbreaks."
        }