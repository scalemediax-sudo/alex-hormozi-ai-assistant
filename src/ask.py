from __future__ import annotations

import argparse
import json
import math
import os
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data" / "index.jsonl"
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
    "how", "i", "in", "is", "it", "me", "my", "of", "on", "or", "our",
    "that", "the", "this", "to", "we", "what", "with", "you", "your",
}


def tokenize(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-zA-Z0-9$]+", text.lower())
        if token not in STOPWORDS and len(token) > 1
    ]


def load_index() -> list[dict]:
    if not INDEX_PATH.exists():
        raise SystemExit("Index not found. Run: python src/build_index.py")
    with INDEX_PATH.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def retrieve(query: str, records: list[dict], limit: int) -> list[dict]:
    query_terms = Counter(tokenize(query))
    if not query_terms:
        return []

    doc_freq: Counter[str] = Counter()
    tokenized = []
    for record in records:
        terms = Counter(tokenize(record["text"] + " " + record["source"]))
        tokenized.append(terms)
        doc_freq.update(terms.keys())

    total_docs = len(records)
    scored = []
    for record, terms in zip(records, tokenized):
        score = 0.0
        for term, query_count in query_terms.items():
            if term not in terms:
                continue
            idf = math.log((1 + total_docs) / (1 + doc_freq[term])) + 1
            score += query_count * terms[term] * idf
        if score:
            scored.append((score, record))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [record for _, record in scored[:limit]]


def answer_with_openai(question: str, contexts: list[dict]) -> str:
    from openai import OpenAI

    context_text = "\n\n".join(
        f"Source: {item['source']} chunk {item['chunk']}\n{item['text']}"
        for item in contexts
    )
    system = (
        "You are a business strategy assistant trained on a Hormozi-style "
        "knowledge base. You are not Alex Hormozi and are not affiliated with "
        "him. Give practical, direct advice. Use the provided context only as "
        "source material, cite source filenames, and do not fabricate quotes."
    )
    user = f"Question: {question}\n\nRetrieved context:\n{context_text}"

    client = OpenAI()
    response = client.responses.create(
        model=DEFAULT_MODEL,
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return response.output_text


def print_contexts(contexts: list[dict]) -> None:
    for index, item in enumerate(contexts, start=1):
        excerpt = item["text"][:900].strip()
        if len(item["text"]) > 900:
            excerpt += "..."
        print(f"\n[{index}] {item['source']} chunk {item['chunk']}\n{excerpt}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("question", help="Question to ask the knowledge base")
    parser.add_argument("--top-k", type=int, default=6)
    parser.add_argument("--no-ai", action="store_true", help="Only print retrieved excerpts")
    args = parser.parse_args()

    records = load_index()
    contexts = retrieve(args.question, records, args.top_k)
    if not contexts:
        raise SystemExit("No relevant context found.")

    if args.no_ai or not os.getenv("OPENAI_API_KEY"):
        print("Retrieved context. Set OPENAI_API_KEY for generated answers.")
        print_contexts(contexts)
        return

    print(answer_with_openai(args.question, contexts))


if __name__ == "__main__":
    main()
