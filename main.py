"""DocuChat command line.

Usage:
    python main.py ingest              # build the FAISS index from data/sample_docs
    python main.py chat                # interactive chat loop
    python main.py ask "your question"  # single question
    python main.py evaluate            # run the sample evaluation set
"""
import sys

from src.config import validate
from src.ingest import build_index


def cmd_ingest() -> None:
    build_index()


def cmd_chat() -> None:
    from src.rag import RagChatbot

    bot = RagChatbot()
    print("DocuChat ready. Ask questions about your documents (type 'exit' to quit).\n")
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        if question.lower() in {"exit", "quit"}:
            print("Bye!")
            break
        if not question:
            continue
        result = bot.ask(question)
        print(f"\nDocuChat: {result['answer']}")
        print(f"(sources: {', '.join(result['sources'])})\n")


def cmd_ask(question: str) -> None:
    from src.rag import RagChatbot

    result = RagChatbot().ask(question)
    print(result["answer"])
    print(f"\nSources: {', '.join(result['sources'])}")


def cmd_evaluate() -> None:
    from src.evaluate import run_evaluation

    report_path = run_evaluation()
    print(f"Evaluation report written to {report_path}")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    validate()
    command = sys.argv[1]
    if command == "ingest":
        cmd_ingest()
    elif command == "chat":
        cmd_chat()
    elif command == "ask" and len(sys.argv) > 2:
        cmd_ask(" ".join(sys.argv[2:]))
    elif command == "evaluate":
        cmd_evaluate()
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
