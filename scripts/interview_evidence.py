#!/usr/bin/env python3
"""One-page interview evidence sheet. Run before every interview."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMANDS = [
    ("Sample gate", [sys.executable, "analysis/compare.py"]),
    ("Contract", [sys.executable, "code/evaluation/main.py"]),
    ("Negative controls", [sys.executable, "analysis/test_eval_negative.py"]),
    ("State tests", [sys.executable, "-m", "unittest", "discover",
                     "-s", "code/tests", "-t", "code"]),
    ("Activity coverage", [sys.executable, "analysis/activity_coverage.py"]),
    ("Activity corroboration", [sys.executable, "analysis/activity_corroboration.py"]),
    ("Attribution split", [sys.executable, "analysis/attribute_split.py"]),
    ("N/A traps", [sys.executable, "analysis/na_traps.py"]),
    ("Break-even", [sys.executable, "analysis/breakeven.py"]),
]


def main() -> int:
    for title, command in COMMANDS:
        print(f"\n=== {title} ===")
        print("$", " ".join(command[1:]))
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        output = (result.stdout or "") + (result.stderr or "")
        print("\n".join(output.strip().splitlines()[-12:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
