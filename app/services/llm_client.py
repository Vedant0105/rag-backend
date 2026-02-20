import os
import requests
import time

GROQ_API_KEY = os.getenv("GEMINI_API_KEY")  # ✅ correct env var
GROQ_URL = os.getenv("GROQ_URL")     # ✅ correct URL


class LLMException(Exception):
    """Raised when the LLM call fails."""
    pass


def build_rag_prompt(question: str, context_chunks: list[str]) -> str:
    """
    Construct grounded RAG prompt.
    """
    context_text = "\n\n".join(context_chunks)
    prompt = f"""
You are a helpful assistant.
Answer the question ONLY using the provided context.
If the answer is not in the context, say "I don't know based on the document."

Context:
{context_text}

Question:
{question}

Answer:
"""
    return prompt.strip()


def call_external_llm(prompt: str, retries: int = 3) -> str:
    """
    Call Groq API with retry + exponential backoff.
    Raises LLMException on failure instead of returning error strings.
    """
    if not GROQ_API_KEY:
        raise LLMException("Groq API key not configured.")

    for attempt in range(retries):
        try:
            response = requests.post(
                GROQ_URL,  # ✅ no ?key= appended
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",  # ✅ Bearer token
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",  # ✅ Groq model
                    "messages": [
                        {"role": "user", "content": prompt}  # ✅ Groq message format
                    ],
                    "temperature": 0.2,
                },
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]  # ✅ Groq response format

        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 429:
                if attempt < retries - 1:
                    wait_time = 5 * (2 ** attempt)
                    print(f"⚠️ Rate limited. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                raise LLMException("Groq rate limit exceeded after retries.")
            raise LLMException(f"Groq HTTP error: {str(e)}")

        except requests.exceptions.Timeout:
            raise LLMException("Groq request timed out.")

        except Exception as e:
            raise LLMException(f"Groq call failed: {str(e)}")

    raise LLMException("Groq call failed after all retries.")