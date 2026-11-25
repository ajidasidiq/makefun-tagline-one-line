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
    # Guard the point of the line: it must name the agents, the bounties
    # they enter, and the best entry winning the reward. A tagline that
    # loses any of those could sell any site, not make.fun.
    lowered = line.lower()
    for needed in ("agent", "bount", "best", "reward"):
        if needed not in lowered:
            print(f"tagline missing required idea: {needed}", file=sys.stderr)
            return 1
    dest_dir = output_dir()
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "entry.txt")
    # Write atomically and read back, so a crash can never leave a
    # half-written entry behind and the file on disk is exactly the line.
    tmp = dest + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    os.replace(tmp, dest)
    with open(dest, "r", encoding="utf-8", newline="") as handle:
        if handle.read() != line:
            print("read-back mismatch", file=sys.stderr)
            return 1
    print(line)
    print(f"wrote {dest} ({len(line)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
