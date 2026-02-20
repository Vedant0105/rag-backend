import os
from pypdf import PdfReader


def extract_text_from_txt(file_path: str) -> str:
    """Read text from txt file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF."""
    reader = PdfReader(file_path)

    text_pages = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_pages.append(page_text)

    return "\n".join(text_pages)


def load_file(file_path: str, filename: str) -> str:
    """
    Detect file type and extract text.
    """
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".txt":
        return extract_text_from_txt(file_path)

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)

    raise ValueError(f"Unsupported file type: {ext}")
