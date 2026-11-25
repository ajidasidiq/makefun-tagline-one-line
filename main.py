"""make.fun tagline entry.

Writes one line -- the tagline for make.fun -- to entry.txt inside the
harness output directory, exactly as the program/v1 harness expects it.
"""

import os
import sys

TAGLINE = (
    "Agents enter bounties. "
    "The best entry wins the reward, scored and paid in the open."
)

MAX_CHARS = 100


def output_dir() -> str:
    """Harness output dir: MAKEFUN_OUTPUT_DIR when set, else /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main() -> int:
    line = TAGLINE.strip()
    if not line or len(line) > MAX_CHARS:
        print(f"tagline invalid: {len(line)} chars", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("tagline must be a single line", file=sys.stderr)
        return 1
    dest_dir = output_dir()
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "entry.txt")
    with open(dest, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    print(line)
    print(f"wrote {dest} ({len(line)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
