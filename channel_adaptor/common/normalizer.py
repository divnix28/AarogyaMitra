from channel_adaptor.common.message_schema import CommonMessage
import datetime

def normalize_message(
    user_id: str,
    text: str,
    channel: str = "whatsapp",
    message_id: str = None,
    timestamp: str = None,
    phone_number: str = None,
    language: str = "en",
) -> CommonMessage:
    if not text or not text.strip():
        raise ValueError("Message text cannot be empty")

    return CommonMessage(
        user_id=user_id,
        message=text.strip(),  # Mapped to 'message' for backend compatibility
        channel=channel,
        message_id=message_id,
        timestamp=timestamp or datetime.datetime.now(datetime.timezone.utc).isoformat(),
        phone_number=phone_number or user_id,
        language=language or "en",
    )
