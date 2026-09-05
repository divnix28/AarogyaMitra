import sys
import os
import requests

# Add root directory to Python path to allow cross-module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

# --- LLM Integration (Groq via OpenAI SDK) ---
try:
    from openai import OpenAI
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        # Point the standard OpenAI client to Groq's API
        llm_client = OpenAI(
            api_key=groq_key,
            base_url="https://api.groq.com/openai/v1"
        )
    else:
        llm_client = None
except ImportError:
    llm_client = None

def generate_llm_response(user_message, context, intent):
    """Generates the final response using trusted RAG context."""
    if not llm_client:
        print("\n[DEBUG] LLM fallback: GROQ_API_KEY missing or client not initialized.\n")
        return f"System processed: '{user_message}'. Retrieved evidence: {context}"
    
    prompt = f"""
    You are AarogyaMitra, a reliable health assistant.
    Intent: {intent}
    Trusted Medical Context: {context}
    
    Answer the user's query safely and simply using ONLY the provided medical context.
    User Query: {user_message}
    """
    try:
        # Swap to Groq's hosted Llama 3 model
        response = llm_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=250
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"\n[DEBUG] LLM fallback triggered by API Error:\n{str(e)}\n")
        return f"System processed: '{user_message}'. Retrieved evidence: {context}"

# --- Member 3 (Rasa NLU) ---
def get_rasa_intent(user_message):
    try:
        response = requests.post(
            "http://localhost:5005/model/parse",
            json={"text": user_message},
            timeout=3
        )
        if response.status_code == 200:
            return response.json().get("intent", {}).get("name", "disease_awareness")
    except Exception:
        pass
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
    
    # 1. NLU / Intent 
    intent_result = get_rasa_intent(user_message)
    
    # 2. RAG Retrieval 
    retrieval_result = mock_retrieve(user_message)
    context = retrieval_result.get("context", "No context found.")
    
    # 3. LLM Generation
    generated_answer = generate_llm_response(user_message, context, intent_result)
    
    # 4. Safety & HRRS 
    safety_check = validate_message(generated_answer)
    hrrs_score = calculate_score(intent_result, context)
    
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
