from typing import List, Dict, Any

def chunk_document(
    text: str, 
    source_metadata: Dict[str, Any], 
    chunk_size: int = 500, 
    overlap: int = 50
) -> List[Dict[str, Any]]:
    words = text.split()
    chunks = []
    
    if not words:
        return chunks

    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i:i + chunk_size]
        chunk_text = " ".join(chunk_words)
        
        chunk_id = f"{source_metadata.get('source_id', 'doc')}_chunk_{len(chunks)}"
        
        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text,
            "metadata": source_metadata
        })
        
        if i + chunk_size >= len(words):
            break
            
    return chunks