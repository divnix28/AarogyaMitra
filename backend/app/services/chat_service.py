import sys
import os
import requests

# Add root directory to Python path to allow cross-module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

# --- Member 3 (Rasa NLU) ---
def get_rasa_intent(user_message):
    """Fetches intent from Member 3's Rasa NLU server"""
    try:
        # Calls the local Rasa NLP server (default port 5005)
        response = requests.post(
            "http://localhost:5005/model/parse",
            json={"text": user_message},
            timeout=3
        )
        if response.status_code == 200:
            return response.json().get("intent", {}).get("name", "disease_awareness")
    except Exception:
        pass # Failsafe if Rasa is offline
    return "disease_awareness"

# --- Member 4 (RAG) Imports ---
try:
    from rag.retrieval.retrieval import mock_retrieve
except ImportError:
    def mock_retrieve(query):
        return {"context": "Mock fallback context", "sources": [], "retrieval_quality": 0.0, "insufficient_evidence": True}

# --- Member 5 (Safety & HRRS) Imports ---
try:
    from hrrs.calculator import calculate_score
    from safety.safety_validator import validate_message
except ImportError:
    def calculate_score(intent, context):
        return 85
    def validate_message(message):
        return {"action": "ANSWER", "flagged": False}

def process_chat_pipeline(request_data):
    """
    Central pipeline: Understand -> Retrieve -> Generate -> Validate (Safety/HRRS)
    """
    user_message = request_data.message
    
    # 1. NLU / Intent (Member 3 Integration)
    intent_result = get_rasa_intent(user_message)
    
    # 2. RAG Retrieval (Member 4 Integration)
    retrieval_result = mock_retrieve(user_message)
    context = retrieval_result.get("context", "No context found.")
    
    # 3. LLM Generation (Placeholder)
    generated_answer = f"System processed: '{user_message}'. Retrieved evidence: {context}"
    
    # 4. Safety & HRRS (Member 5 Integration)
    safety_check = validate_message(generated_answer)
    hrrs_score = calculate_score(intent_result, context)
    
    # Override action if risk score is critically high
    action = safety_check.get("action", "ANSWER")
    if hrrs_score >= 90:
        action = "ESCALATE_TO_HUMAN"
        generated_answer = "This query requires human assistance. Escalating to a medical professional."
    
    return {
        "message": generated_answer,
        "intent": intent_result,
        "confidence": 0.95,
        "action": action,
        "hrrs_score": hrrs_score,
        "sources": retrieval_result.get("sources", [])
    }