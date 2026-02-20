import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = "RAG Chatbot"
    API_V1_STR: str = "/api"

    # upload
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "uploads")

    # chunking
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 100

    # retrieval
    TOP_K: int = 4

settings = Settings()
