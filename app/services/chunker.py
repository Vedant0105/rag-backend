import re
from typing import List
from app.core.config import settings


def clean_text(text: str) -> str:
    """Basic text cleanup."""
    text = text.replace("\r", "\n")
    text = "\n".join(line.strip() for line in text.splitlines())
    text = "\n".join(line for line in text.splitlines() if line)
    return text.strip()


def split_into_sentences(text: str) -> List[str]:
    """
    Simple sentence splitter.
    Fast and good enough for resumes/docs.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(text: str) -> List[str]:
    """
    ✅ Sentence-aware chunking
    ✅ With overlap
    ✅ Production friendly
    """

    text = clean_text(text)
    sentences = split_into_sentences(text)

    chunk_size = settings.CHUNK_SIZE
    overlap = settings.CHUNK_OVERLAP

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If adding sentence exceeds chunk size → push chunk
        if len(current_chunk) + len(sentence) + 1 > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())

                # 🔥 create overlap from end of previous chunk
                if overlap > 0:
                    current_chunk = current_chunk[-overlap:]
                else:
                    current_chunk = ""

        current_chunk += sentence + " "

    # add last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks
