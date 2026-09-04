import sys
import os

# Add root directory to Python path to allow cross-module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

try:
    from rag.retrieval.retriever import mock_retrieve
except ImportError:
    # Failsafe if Member 4's file structure isn't exactly as expected
    def mock_retrieve(query):
        return {
            "context": "Mock fallback context", 
            "sources": [], 
            "retrieval_quality": 0.0, 
            "insufficient_evidence": True
        }

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
    
    # 4. Safety & HRRS (Member 5 Placeholder)
    hrrs_score = 85
    action = "ANSWER"
    
    return {
        "message": generated_answer,
        "intent": mock_intent,
        "confidence": 0.95,
        "action": action,
        "hrrs_score": hrrs_score,
        "sources": retrieval_result.get("sources", [])
    }
