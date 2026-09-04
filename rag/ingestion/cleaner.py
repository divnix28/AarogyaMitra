import re

def clean_medical_text(text: str) -> str:
    """
    Cleans text while preserving medical negation, dosages, and units.
    NEVER strips 'not', 'no', 'never', or numerical quantities.
    """
    if not text:
        return ""
    
    # 1. Normalize line endings and repetitive spaces
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    # 2. Preserve structural lists and line breaks
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()