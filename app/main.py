from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

# CORS (important for React later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger(__name__).info("✅ App started and ready.")