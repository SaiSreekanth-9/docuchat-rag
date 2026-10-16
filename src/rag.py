"""RAG answering: retrieve top-k chunks, stuff them into a grounded prompt, generate."""
import os

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from .config import settings, validate

SYSTEM_PROMPT = """You are DocuChat, a helpful assistant that answers questions strictly from the provided context.

Rules:
1. Use ONLY the context below. If the answer is not in the context, say "I don't know based on the provided documents."
2. Be concise and direct.
3. When you state a fact, cite the source document in brackets, e.g. [company_handbook.md].
4. Never invent details that are not in the context."""

_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"),
    ]
)


def _format_docs(docs) -> str:
    parts = []
    for doc in docs:
        name = os.path.basename(doc.metadata.get("source", "unknown"))
        parts.append(f"--- Source: {name} ---\n{doc.page_content}")
    return "\n\n".join(parts)


class RagChatbot:
    """Loads the persisted FAISS index once, answers questions with citations."""

    def __init__(self) -> None:
        validate()
        embeddings = OpenAIEmbeddings(
            model=settings.embedding_model, api_key=settings.openai_api_key
        )
        self.store = FAISS.load_local(
            settings.index_dir, embeddings, allow_dangerous_deserialization=True
        )
        self.retriever = self.store.as_retriever(search_kwargs={"k": settings.top_k})
        self.llm = ChatOpenAI(
            model=settings.chat_model, temperature=0, api_key=settings.openai_api_key
        )
        # A small LCEL chain: prompt -> model. Retrieval is done explicitly above
        # so the flow stays transparent and easy to debug.
        self.chain = _prompt | self.llm

    def ask(self, question: str) -> dict:
        """Return the answer plus the sources it was grounded in."""
        docs = self.retriever.invoke(question)
        context = _format_docs(docs)
        answer = self.chain.invoke({"context": context, "question": question}).content
        sources = sorted(
            {os.path.basename(d.metadata.get("source", "unknown")) for d in docs}
        )
        return {"answer": answer, "sources": sources, "num_chunks": len(docs)}
