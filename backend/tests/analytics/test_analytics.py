from unittest.mock import patch
from app.analytics.symptom_trends import detect_symptom_surge
from app.analytics.phix import PHIXEngine

def test_detect_symptom_surge():
    # Setup mock current counts and baseline historical data
    current_counts = {"fever": 10, "cough": 4, "rash": 6}
    historical_averages = {"fever": 3.0, "cough": 2.0} 
    # 'rash' is omitted from historical to test the 0.0 default fallback
    
    surges = detect_symptom_surge(current_counts, historical_averages)
    
    # fever: 10 > (3.0 + 5.0) -> True
    assert surges["fever"] == True
    # cough: 4 > (2.0 + 5.0) -> False
    assert surges["cough"] == False
    # rash: 6 > (0.0 + 5.0) -> True
    assert surges["rash"] == True

@patch("app.analytics.phix.aggregate_daily_topics")
def test_phix_engine_generate_signals(mock_aggregate):
    # Mock the aggregation output to isolate and test PHIXEngine logic
    mock_aggregate.return_value = {"fever": 12, "fatigue": 3}
    
    engine = PHIXEngine()
    historical_data = {"fever": 5.0, "fatigue": 2.0}
    
    # recent_interactions is passed as an empty list since the aggregation is mocked
    result = engine.generate_early_signals(recent_interactions=[], historical_data=historical_data)
    
    assert result["status"] == "success"
    assert result["aggregated_counts"] == {"fever": 12, "fatigue": 3}
    assert result["detected_surges"]["fever"] == True  # 12 > (5.0 + 5.0)
    assert result["detected_surges"]["fatigue"] == False  # 3 > (2.0 + 5.0)
    assert "early community intelligence signals" in result["disclaimer"]