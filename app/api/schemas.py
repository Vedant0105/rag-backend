from pydantic import BaseModel
from typing import Literal, List, Optional

class ChatRequest(BaseModel):
    question: str
    mode: Literal["rag", "file_only"] = "rag"

class ChatResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None

class UploadResponse(BaseModel):
    message: str
    filename: str
