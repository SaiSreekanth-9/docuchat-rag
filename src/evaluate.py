"""Simple evaluation: run fixed questions, record answers + sources to a report."""
from datetime import datetime, timezone
from pathlib import Path

from .rag import RagChatbot

TEST_QUESTIONS = [
    "How many vacation days do employees get per year?",
    "What is the company's remote work policy?",
    "What should I do if I suspect a phishing email?",
    "What is included in the Pro pricing tier?",
    "How long is customer data retained after cancellation?",
]


def run_evaluation(output_path: str = "examples/eval_report.md") -> str:
    bot = RagChatbot()
    lines = [
        "# DocuChat evaluation report",
        f"_Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}_\n",
    ]
    for i, question in enumerate(TEST_QUESTIONS, 1):
        result = bot.ask(question)
        lines.append(f"## Q{i}: {question}")
        lines.append(f"**Answer:** {result['answer']}\n")
        lines.append(f"**Sources:** {', '.join(result['sources'])}")
        lines.append(f"**Chunks retrieved:** {result['num_chunks']}\n")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text("\n".join(lines), encoding="utf8")
    return output_path
