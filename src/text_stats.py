#!/usr/bin/env python3
"""Count lines, words, and characters in a UTF-8 text file."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*")


def count_text_stats(text: str) -> dict[str, int]:
    """Return the number of lines, words, and characters in a text string."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = len(normalized.splitlines()) if normalized else 0
    words = len(re.findall(r"\S+", normalized))
    characters = len(normalized)
    return {"lines": lines, "words": words, "characters": characters}


def count_top_words(text: str, limit: int) -> list[list[str | int]]:
    """Return the most frequent words as [word, count] pairs in deterministic order."""
    if limit <= 0:
        return []

    counts = Counter(word.lower() for word in WORD_RE.findall(text))
    return [
        [word, count]
        for word, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]
    ]


def _parse_args(argv: list[str]) -> tuple[str | None, int | None]:
    file_path = None
    top_count = None
    index = 0

    while index < len(argv):
        arg = argv[index]

        if arg == "--top":
            if index + 1 >= len(argv):
                raise ValueError("Missing value for --top")
            try:
                top_count = int(argv[index + 1])
            except ValueError as exc:
                raise ValueError("--top requires an integer value") from exc
            index += 2
            continue

        if arg.startswith("--top="):
            try:
                top_count = int(arg.split("=", 1)[1])
            except ValueError as exc:
                raise ValueError("--top requires an integer value") from exc
            index += 1
            continue

        if arg in {"-h", "--help"}:
            print("Usage: python src/text_stats.py <file> [--top N]", file=sys.stderr)
            raise SystemExit(0)

        if arg.startswith("-"):
            raise ValueError(f"Unsupported option: {arg}")

        if file_path is not None:
            raise ValueError("Only one file path is allowed")

        file_path = arg
        index += 1

    if file_path is None:
        raise ValueError("Missing file path")

    return file_path, top_count


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv

    try:
        file_path, top_count = _parse_args(args)
    except SystemExit:
        raise
    except ValueError as exc:
        print("Usage: python src/text_stats.py <file> [--top N]", file=sys.stderr)
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if top_count is not None and top_count < 0:
        print("Usage: python src/text_stats.py <file> [--top N]", file=sys.stderr)
        print("Error: --top must be a non-negative integer", file=sys.stderr)
        return 1

    file_obj = Path(file_path)

    try:
        text = file_obj.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Error reading '{file_obj}': {exc}", file=sys.stderr)
        return 1

    stats = count_text_stats(text)
    if top_count is not None:
        stats["top_words"] = count_top_words(text, top_count)

    print(json.dumps(stats))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
