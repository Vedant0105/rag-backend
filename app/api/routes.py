import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.config import settings
from app.services.file_loader import load_file
from app.api.schemas import ChatRequest, ChatResponse, UploadResponse
from app.services.chunker import chunk_text
from app.services.embeddings import embed_texts
from app.services.vector_store import vector_store
from app.services.retriever import retrieve_relevant_chunks
from app.services.llm_client import build_rag_prompt, call_external_llm, LLMException
from app.services.text_extractor import extract_answer_from_chunks

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = load_file(file_path, file.filename)

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text found in file.")

        chunks = chunk_text(text)

        if not chunks:
            raise HTTPException(status_code=400, detail="Chunking failed.")

        embeddings = embed_texts(chunks)
        vector_store.add_embeddings(embeddings, chunks)

        return UploadResponse(
            message=f"File processed. Extracted {len(text)} chars into {len(chunks)} chunks.",
            filename=file.filename,
        )

    except HTTPException:
        raise  # re-raise validation errors as-is

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        chunks = retrieve_relevant_chunks(request.question)

        if not chunks:
            return ChatResponse(
                answer="No relevant information found in the uploaded document.",
                sources=[],
            )

        # 🔵 MODE 1 — file only (no LLM)
        if request.mode == "file_only":
            answer = extract_answer_from_chunks(request.question, chunks)
            return ChatResponse(answer=answer, sources=chunks)

        # 🟢 MODE 2 — full RAG
        refined_context = extract_answer_from_chunks(request.question, chunks)
        context_for_llm = [refined_context] + chunks[:2]
        prompt = build_rag_prompt(request.question, context_for_llm)

        try:
            answer = call_external_llm(prompt)
        except LLMException as e:
            raise HTTPException(status_code=503, detail=str(e))

        return ChatResponse(answer=answer, sources=chunks)

    except HTTPException:
        raise  # re-raise 503 and other HTTP errors as-is

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))