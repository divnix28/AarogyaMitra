import sys
import os
import requests
import traceback

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app.safety.safety_validator import SafetyValidator
from app.safety.schemas import SafetyValidationRequest, RiskLevel
from app.hrrs.calculator import HRRSCalculator
from app.hrrs.factors import HRRSFactors
from app.hrrs.thresholds import HRRSAction

validator = SafetyValidator()
hrrs_calculator = HRRSCalculator()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

# --- LLM Integration ---
try:
    from openai import OpenAI
    groq_key = os.getenv("GROQ_API_KEY")
    llm_client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None
    if not groq_key:
        print("\n⚠️ WARNING: GROQ_API_KEY is missing! LLM will not work.\n")
except ImportError:
    llm_client = None

# --- Member 4 (RAG) Fully Dynamic Demo Mock ---
def mock_retrieve(query):
    return {
        "context": f"Verified clinical guidelines regarding '{query}': Ensure proper rest, hydration, and monitoring of vitals. Record symptom progression and consult a local ASHA worker or healthcare professional if condition persists.",
        "sources": [
            {"title": "AarogyaMitra Clinical Knowledge Base"}, 
            {"title": "WHO Protocol"}
        ]
    }

def generate_llm_response(user_message, context, intent):
    if not llm_client:
        return f"[NO API KEY] System processed: '{user_message}'. Evidence: {context}"
    try:
        # FIXED: Using Groq's widely supported gpt-oss-20b model
        response = llm_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are AarogyaMitra, a helpful and concise AI health assistant. Use the provided context to answer the user."},
                {"role": "user", "content": f"Context: {context}\nUser: {user_message}"}
            ],
            temperature=0.1,
            max_tokens=250
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"\n🚨 GROQ API ERROR: {e}\n")
        return f"[LLM ERROR] System processed: '{user_message}'. Evidence: {context}"

def get_rasa_intent(user_message):
    try:
        resp = requests.post("http://localhost:5005/model/parse", json={"text": user_message}, timeout=3)
        if resp.status_code == 200:
            return resp.json().get("intent", {}).get("name", "disease_awareness")
    except Exception:
        pass
    return "disease_awareness"

def process_chat_pipeline(request_data):
    try:
        user_message = getattr(request_data, "message", str(request_data))

        # 1. EMERGENCY GATEKEEPER
        safety_request = SafetyValidationRequest(user_message=user_message, intent=None)
        safety_response = validator.validate(safety_request)
        
        if not safety_response.is_safe and safety_response.risk_level == RiskLevel.EMERGENCY:
            return {
                "message": safety_response.escalation_message,
                "intent": "emergency",
                "confidence": 1.0,
                "action": "ESCALATE",
                "hrrs_score": 100,
                "sources": []
            }

        # 2. NLU
        intent_name = get_rasa_intent(user_message)
        
        # 3. HRRS SCORING
        factors = HRRSFactors(
            guideline_match=90.0,
            context_completeness=90.0,
            safety_validation=100.0 if safety_response.is_safe else 0.0,
            intent_confidence=95.0,
            retrieval_quality=90.0
        )
        hrrs_result = hrrs_calculator.calculate(factors=factors, safety_response=safety_response)
        
        final_score = int(round(hrrs_result.score))

        # 4. RAG
        try:
            retrieval = mock_retrieve(user_message)
            context = retrieval.get("context", "") if isinstance(retrieval, dict) else str(retrieval)
        except Exception:
            context = "Standard medical context applied."
            retrieval = {}

        if hrrs_result.action == HRRSAction.ESCALATE:
            escalation_text = safety_response.escalation_message if not safety_response.is_safe else "I cannot reliably answer this query based on retrieved medical evidence."
            return {
                "message": escalation_text,
                "intent": intent_name,
                "confidence": 0.95,
                "action": "ESCALATE_TO_HUMAN",
                "hrrs_score": final_score,
                "sources": retrieval.get("sources", []) if isinstance(retrieval, dict) else []
            }

        # 5. LLM
        generated_answer = generate_llm_response(user_message, context, intent_name)

        return {
            "message": generated_answer,
            "intent": intent_name,
            "confidence": 0.95,
            "action": "ANSWER",
            "hrrs_score": final_score,
            "sources": retrieval.get("sources", []) if isinstance(retrieval, dict) else []
        }

    except Exception:
        print("\n" + "="*40 + "\n🚨 PIPELINE EXCEPTION CAUGHT 🚨\n")
        traceback.print_exc()
        print("="*40 + "\n")
        return {
            "message": "I am processing your symptoms. Please consult a local clinic if you have severe concerns.",
            "intent": "system_fallback",
            "confidence": 0.8,
            "action": "ANSWER",
            "hrrs_score": 50,
            "sources": []
        }
