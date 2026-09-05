def format_response(text: str) -> str:
    """
    Format AarogyaMitra's response for SMS.

    SMS messages should be concise and plain text.
    """

    if not text:
        return "Sorry, I was unable to generate a response."

    return text.strip()