"""Warning label for humans: one line, big laugh.

Writes a single-line safety warning label — the kind that should come
printed on every human being — to entry.txt in the output directory.
Deterministic: the same line is written on every run.
Standard library only, no network access, no reads outside the repo.
"""

import hashlib
import os
from pathlib import Path

MAX_LENGTH = 160

LABEL = (
    "WARNING: This human runs on coffee and 3% battery \u2014 "
    "do not shake, do not ask about work, and handle only with snacks."
)


def validate(text: str) -> None:
    """Check the label meets the competition rules."""
    if not isinstance(text, str) or not text:
        raise ValueError("label must be non-empty text")
    if "\n" in text or "\r" in text:
        raise ValueError("label must be exactly one line")
    if text != text.strip():
        raise ValueError("label must not have leading or trailing whitespace")
    if not 1 <= len(text) <= MAX_LENGTH:
        raise ValueError(f"label must be 1 to {MAX_LENGTH} characters long")
    text.encode("utf-8")  # reject anything that is not valid UTF-8 text


def main() -> None:
    validate(LABEL)
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "entry.txt"
    target.write_text(LABEL, encoding="utf-8")
    # Round-trip check: what landed on disk must be exactly the label.
    if target.read_text(encoding="utf-8") != LABEL:
        raise ValueError("written file does not match the label")
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(digest)


if __name__ == "__main__":
    main()
