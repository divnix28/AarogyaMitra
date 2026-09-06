import httpx


# API configuration will be added later.
SMS_API_URL = "YOUR_SMS_API_URL"
SMS_API_KEY = "YOUR_SMS_API_KEY"
SMS_SENDER_ID = "YOUR_SMS_SENDER_ID"


async def send_message(recipient: str, message: str):
    """
    Send an SMS through the configured SMS provider.
    """

    headers = {
        "Authorization": f"Bearer {SMS_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "sender": SMS_SENDER_ID,
        "recipient": recipient,
        "message": message,
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            SMS_API_URL,
            headers=headers,
            json=payload,
            timeout=10,
        )

    response.raise_for_status()

    return response.json()