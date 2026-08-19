from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRS = [
    ROOT / "course-transcripts",
    ROOT / "course-videos",
    ROOT / "playbooks",
    ROOT / "prompts",
    ROOT / "demos",
]
OUT_PATH = ROOT / "data" / "index.jsonl"
CHUNK_WORDS = 420
OVERLAP_WORDS = 70


def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunks(text: str) -> list[str]:
    words = text.split()
    if not words:
        return []

    step = max(1, CHUNK_WORDS - OVERLAP_WORDS)
    out = []
    for start in range(0, len(words), step):
        part = words[start : start + CHUNK_WORDS]
        if len(part) < 40 and out:
            break
        out.append(" ".join(part))
    return out


def iter_files() -> list[Path]:
    files: list[Path] = []
    for source_dir in SOURCE_DIRS:
        if source_dir.exists():
            files.extend(source_dir.rglob("*.txt"))
            files.extend(source_dir.rglob("*.md"))
            files.extend(source_dir.rglob("*.tsv"))
    return sorted(set(files))


def main() -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    count = 0

    with OUT_PATH.open("w", encoding="utf-8") as out:
        for path in iter_files():
            text = normalize(path.read_text(encoding="utf-8", errors="replace"))
            rel = path.relative_to(ROOT).as_posix()
            for index, chunk in enumerate(chunks(text)):
                record = {
                    "id": f"{rel}#{index}",
                    "source": rel,
                    "chunk": index,
                    "text": chunk,
                }
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1

    print(f"Indexed {count} chunks into {OUT_PATH}")


if __name__ == "__main__":
    main()
