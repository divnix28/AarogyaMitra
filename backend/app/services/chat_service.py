import sys
import os

# Add root directory to Python path to allow cross-module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

# --- Member 4 (RAG) Imports ---
try:
    from rag.retrieval.retriever import mock_retrieve
except ImportError:
    def mock_retrieve(query):
        return {"context": "Mock fallback context", "sources": [], "retrieval_quality": 0.0, "insufficient_evidence": True}

# --- Member 5 (Safety & HRRS) Imports ---
try:
    # Attempting to load Member 5's newly merged functions
    from hrrs.calculator import calculate_score
    from safety.safety_validator import validate_message
except ImportError:
    # Failsafe if their exact function names differ from the expected contract
    def calculate_score(intent, context):
        return 85
        
    def validate_message(message):
        return {"action": "ANSWER", "flagged": False}

def process_chat_pipeline(request_data):
    """
    Central pipeline: Understand -> Retrieve -> Generate -> Validate (Safety/HRRS)
    """
    user_message = request_data.message
    
    # 1. NLU / Intent (Member 3 Placeholder)
    mock_intent = "disease_awareness"
    
    # 2. RAG Retrieval (Member 4 Integration)
    retrieval_result = mock_retrieve(user_message)
    context = retrieval_result.get("context", "No context found.")
    
    # 3. LLM Generation (Placeholder)
    generated_answer = f"System processed: '{user_message}'. Retrieved evidence: {context}"
    
    # 4. Safety & HRRS (Member 5 Integration)
    safety_check = validate_message(generated_answer)
    hrrs_score = calculate_score(mock_intent, context)
    
    # Override action if risk score is critically high
    action = safety_check.get("action", "ANSWER")
    if hrrs_score >= 90:
        action = "ESCALATE_TO_HUMAN"
        generated_answer = "This query requires human assistance. Escalating to a medical professional."
    
    return {
        "message": generated_answer,
        "intent": mock_intent,
        "confidence": 0.95,
        "action": action,
        "hrrs_score": hrrs_score,
        "sources": retrieval_result.get("sources", [])
    }