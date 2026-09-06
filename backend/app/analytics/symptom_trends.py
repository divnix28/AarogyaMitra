from typing import Dict

def detect_symptom_surge(current_counts: Dict[str, int], historical_averages: Dict[str, float]) -> Dict[str, bool]:
    # Identifies early community signals, NOT clinical outbreak predictions
    surges = {}
    for symptom, count in current_counts.items():
        baseline = historical_averages.get(symptom, 0.0)
        # Flag as a surge if count is significantly higher than the baseline
        surges[symptom] = count > (baseline + 5.0)
    return surges