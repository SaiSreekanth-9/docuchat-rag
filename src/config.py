"""Central configuration for DocuChat. Values come from environment variables / .env."""
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    chat_model: str = os.getenv("CHAT_MODEL", "gpt-4o-mini")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    top_k: int = int(os.getenv("TOP_K", "4"))
    docs_dir: str = os.getenv("DOCS_DIR", "data/sample_docs")
    index_dir: str = os.getenv("INDEX_DIR", "faiss_index")


settings = Settings()


def validate() -> None:
    """Fail fast with a helpful message when the API key is missing."""
    if not settings.openai_api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Copy .env.example to .env and add your OpenAI API key."
        )
