from fastapi import APIRouter, Request, HTTPException

from ..common.normalizer import normalize_message


router = APIRouter(
    prefix="/webhook/sms",
    tags=["SMS"]
)


@router.post("")
async def sms_webhook(request: Request):

    try:

        payload = await request.json()

        user_id = payload.get("from")
        text = payload.get("text")
        message_id = payload.get("message_id")
        timestamp = payload.get("timestamp")

        if not user_id:
            raise HTTPException(
                status_code=400,
                detail="Missing user ID"
            )

        if not text:
            raise HTTPException(
                status_code=400,
                detail="Missing message text"
            )

        message = normalize_message(
            user_id=user_id,
            text=text,
            channel="sms",
            message_id=message_id,
            timestamp=timestamp,
            phone_number=user_id,
        )

        return {
            "status": "received",
            "user_id": message.user_id,
            "text": message.text,
            "channel": message.channel,
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail="Failed to process SMS webhook"
        ) from exc