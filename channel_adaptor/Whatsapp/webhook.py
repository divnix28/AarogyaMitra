def format_response(text: str) -> str:
    """
    Format AarogyaMitra response for WhatsApp.
    """

    if not text:
        return "Sorry, I was unable to generate a response."

    return text.strip()