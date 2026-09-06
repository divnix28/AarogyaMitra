import sys
import os
import requests
from app.safety.safety_validator import SafetyValidator
from app.safety.schemas import SafetyValidationRequest, RiskLevel
from app.hrrs.calculator import HRRSCalculator  # Corrected Import
from app.hrrs.factors import HRRSFactors
from app.hrrs.thresholds import HRRSAction

# Initialize both of Member 5's modules
validator = SafetyValidator()
hrrs_calculator = HRRSCalculator()

# Add root directory to Python path to allow cross-module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

# --- LLM Integration (Groq via OpenAI SDK) ---
try:
    from openai import OpenAI
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
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


def process_chat_pipeline(request_data):
    """
    Central pipeline: Gatekeeper -> Understand -> Risk Score -> Retrieve -> Generate
    """
    user_message = request_data.message

    # --- STEP 1: EMERGENCY GATEKEEPER ---
    safety_request = SafetyValidationRequest(user_message=user_message, intent=None)
    safety_response = validator.validate(safety_request)
    
    if not safety_response.is_safe and safety_response.risk_level == RiskLevel.EMERGENCY:
        return {
            "message": safety_response.escalation_message,
            "intent": "emergency",
            "confidence": 1.0,
            "action": "ESCALATE",
            "hrrs_score": 100.0,
            "sources": []
        }

    # --- STEP 2: NLU / INTENT EXTRACTION ---
    intent_result = get_rasa_intent(user_message)
    # Handle the mock string return vs actual Rasa dict return safely
    intent_name = intent_result if isinstance(intent_result, str) else intent_result.get("name", "unknown")
    confidence = 0.95 if isinstance(intent_result, str) else intent_result.get("confidence", 0.95)
    
    # --- STEP 3: HRRS RISK SCORING ---
    factors = HRRSFactors(
        guideline_match=0.9,
        context_completeness=0.9,
        safety_validation=1.0 if safety_response.is_safe else 0.0,
        intent_confidence=confidence,
        retrieval_quality=0.9
    )
    
    hrrs_result = hrrs_calculator.calculate(factors=factors, safety_response=safety_response)

    if hrrs_result.action == HRRSAction.ESCALATE or hrrs_result.score >= 90:
        return {
            "message": "High clinical risk detected based on your symptoms. Escalating to a medical professional.",
            "intent": intent_name,
            "confidence": confidence,
            "action": "ESCALATE_TO_HUMAN",
            "hrrs_score": hrrs_result.score,
            "sources": []
        }

    # --- STEP 4: RAG RETRIEVAL ---
    retrieval_result = mock_retrieve(user_message) 
    context = retrieval_result.get("context", "No context found.")

    # --- STEP 5: LLM GENERATION ---
    generated_answer = generate_llm_response(user_message, context, intent_name)

    return {
        "message": generated_answer,
        "intent": intent_name,
        "confidence": confidence,
        "action": "ANSWER",
        "hrrs_score": hrrs_result.score,
        "sources": retrieval_result.get("sources", [])
    }
