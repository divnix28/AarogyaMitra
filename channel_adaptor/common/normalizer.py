from .message_schema import CommonMessage


def normalize_message(
    user_id: str,
    text: str,
    channel: str,
    message_id: str = None,
    timestamp: str = None,
    phone_number: str = None,
    language: str = None,
) -> CommonMessage:

    if not text:
        raise ValueError("Message text cannot be empty")

    return CommonMessage(
        user_id=user_id,
        text=text.strip(),
        channel=channel,
        message_id=message_id,
        timestamp=timestamp,
        phone_number=phone_number,
        language=language,
    )