import httpx


async def send_message(
    recipient: str,
    message: str,
    api_url: str,
    access_token: str,
):
    """
    Send a WhatsApp message through the configured provider.
    """

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "to": recipient,
        "text": message,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            api_url,
            json=payload,
            headers=headers,
            timeout=10,
        )

    response.raise_for_status()

    return response.json()