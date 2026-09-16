#!/usr/bin/env python3
"""Count lines, words, and characters in a UTF-8 text file."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def count_text_stats(text: str) -> dict[str, int]:
    """Return the number of lines, words, and characters in a text string."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = len(normalized.splitlines()) if normalized else 0
    words = len(re.findall(r"\S+", normalized))
    characters = len(normalized)
    return {"lines": lines, "words": words, "characters": characters}


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv

    if len(args) != 1:
        print("Usage: python src/text_stats.py <file>", file=sys.stderr)
        return 1

    file_path = Path(args[0])

    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Error reading '{file_path}': {exc}", file=sys.stderr)
        return 1

    stats = count_text_stats(text)
    print(json.dumps(stats))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
