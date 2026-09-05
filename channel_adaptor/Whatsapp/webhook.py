from fastapi import APIRouter, HTTPException
from channel_adaptor.common.normalizer import normalize_message
from channel_adaptor.Whatsapp.formatter import format_response
from app.services.chat_service import process_chat_pipeline

router = APIRouter(prefix="/webhook/whatsapp", tags=["whatsapp"])

@router.post("")
def receive_whatsapp_webhook(payload: dict):
    """
    Receives incoming payload from WhatsApp provider (Meta Cloud / Twilio),
    normalizes it to CommonMessage, and processes directly through the pipeline.
    """
    try:
        user_id = payload.get("From") or payload.get("user_id") or "test_user"
        text = payload.get("Body") or payload.get("message") or ""
        message_id = payload.get("MessageSid") or payload.get("message_id")
        
        # 1. Normalize payload
        normalized_msg = normalize_message(
            user_id=user_id,
            text=text,
            channel="whatsapp",
            message_id=message_id
        )

        # 2. Invoke orchestrator directly (no loopback HTTP overhead)
        result = process_chat_pipeline(normalized_msg)
        
        # 3. Format response for WhatsApp
        formatted_text = format_response(result.get("message", ""))
        
        return {
            "status": "success",
            "reply": formatted_text,
            "action": result.get("action"),
            "intent": result.get("intent")
        }

    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(err)}")
