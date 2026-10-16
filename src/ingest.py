"""Document ingestion: load -> chunk -> embed -> FAISS index on disk."""
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

try:  # langchain-text-splitters is the canonical package since 2024
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:  # fallback for older langchain installs
    from langchain.text_splitter import RecursiveCharacterTextSplitter

from .config import settings, validate


def load_documents(docs_dir: str):
    """Load .md, .txt and .pdf files, keeping the file path in each doc's metadata."""
    docs = []
    for glob, loader in (
        ("**/*.md", TextLoader),
        ("**/*.txt", TextLoader),
        ("**/*.pdf", PyPDFLoader),
    ):
        kwargs = {"encoding": "utf8"} if loader is TextLoader else {}
        docs.extend(
            DirectoryLoader(docs_dir, glob=glob, loader_cls=loader, loader_kwargs=kwargs).load()
        )
    # De-duplicate in case of overlapping globs
    seen = set()
    unique = []
    for doc in docs:
        key = (doc.metadata.get("source"), doc.page_content[:64])
        if key not in seen:
            seen.add(key)
            unique.append(doc)
    return unique


def build_index(docs_dir: str | None = None, index_dir: str | None = None) -> dict:
    """Chunk documents, embed them and persist a FAISS index. Returns build stats."""
    validate()
    docs_dir = docs_dir or settings.docs_dir
    index_dir = index_dir or settings.index_dir

    documents = load_documents(docs_dir)
    if not documents:
        raise FileNotFoundError(f"No .md/.txt/.pdf documents found in '{docs_dir}'.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model, api_key=settings.openai_api_key
    )
    store = FAISS.from_documents(chunks, embeddings)
    Path(index_dir).mkdir(parents=True, exist_ok=True)
    store.save_local(index_dir)

    stats = {
        "documents": len(documents),
        "chunks": len(chunks),
        "index_dir": str(Path(index_dir).resolve()),
        "embedding_model": settings.embedding_model,
    }
    print(
        f"Indexed {stats['chunks']} chunks from {stats['documents']} documents "
        f"-> {stats['index_dir']}"
    )
    return stats
