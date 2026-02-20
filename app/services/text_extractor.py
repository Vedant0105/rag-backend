# app/services/text_extractor.py
from typing import List
import re

def extract_answer_from_chunks(question: str, chunks: List[str], max_sentences: int = 5) -> str:
    """
    Generic extractor:
    - Returns most relevant sentences from chunks based on keyword matches from question.
    - Returns a clean text snippet.
    """
    text = " ".join(chunks)
    text = re.sub(r'\s+', ' ', text)  # normalize spaces

    # Extract keywords from question (simple split + lowercase)
    keywords = [word.lower() for word in re.findall(r'\w+', question)]

    # Score sentences by keyword occurrence
    sentences = re.split(r'(?<=[.!?])\s+', text)
    scored = []
    for sentence in sentences:
        score = sum(1 for kw in keywords if kw in sentence.lower())
        if score > 0:
            scored.append((score, sentence.strip()))

    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)

    # Take top N sentences
    top_sentences = [s for _, s in scored[:max_sentences]]
    return " ".join(top_sentences) if top_sentences else text[:500]  # fallback snippet
