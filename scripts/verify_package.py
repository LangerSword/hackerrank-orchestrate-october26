#!/usr/bin/env python3
"""Build the submission zip, extract it into a clean directory, and run it.

This is the gate that the first submission missed: a package is not ready
because it works in the repository. It is ready when it works after extraction
with no repo files around it.
"""
from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZIP = ROOT / "code-v2.zip"
GENERATED = {"analysis/sample_output.csv", "output.csv"}
EXECUTABLES = {"scripts/fetch_dataset.sh"}


def package_files() -> list[Path]:
    files = [Path("README.md")]
    files += sorted(p for p in Path("code").rglob("*")
                    if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
    files += [
        Path("analysis/compare.py"),
        Path("analysis/test_eval_negative.py"),
        Path("analysis/test_intent.py"),
        Path("analysis/activity_coverage.py"),
        Path("scripts/fetch_dataset.sh"),
        Path("scripts/verify_package.py"),
        Path("scripts/check_claims.py"),
    ]
    files += sorted(Path("docs").glob("*.md"))
    return files


def build() -> None:
    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in package_files():
            info = zipfile.ZipInfo(str(path))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (
                (0o755 if str(path) in EXECUTABLES else 0o644) << 16
            )
            archive.writestr(info, (ROOT / path).read_bytes())


def readme_paths() -> set[str]:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    found = set(re.findall(r"(?:\./)?((?:code|analysis|scripts)/[\w./-]+\.(?:py|sh))", text))
    return {p for p in found if p not in GENERATED}


def run(command: list[str], cwd: Path, needle: str | None = None) -> None:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        print(output)
        raise SystemExit(f"failed ({result.returncode}): {' '.join(command)}")
    if needle and needle not in output:
        print(output)
        raise SystemExit(f"missing {needle!r} in: {' '.join(command)}")


def main() -> int:
    build()
    with zipfile.ZipFile(ZIP) as archive:
        names = archive.namelist()
        if archive.testzip() is not None:
            raise SystemExit("zip integrity failure")
        if any(n.startswith("dataset/") or "__pycache__" in n or n.endswith(".pyc")
               for n in names):
            raise SystemExit("zip contains dataset or caches")
        if any(n.lower().endswith((".zip", ".tar", ".gz", ".tgz", ".7z", ".rar")) for n in names):
            raise SystemExit("zip contains a nested archive")
        missing = sorted(readme_paths() - set(names))
        if missing:
            raise SystemExit(f"README references missing files: {missing}")

    with tempfile.TemporaryDirectory(prefix="orchestrate-package-") as tmp:
        work = Path(tmp) / "entry"
        work.mkdir()
        with zipfile.ZipFile(ZIP) as archive:
            archive.extractall(work)
        os.chmod(work / "scripts/fetch_dataset.sh", 0o755)
        dataset = ROOT / "dataset"
        if not (dataset / "deletion_requests.csv").exists():
            raise SystemExit("dataset/ is missing in the source checkout")
        (work / "dataset").symlink_to(dataset)

        run(["./scripts/fetch_dataset.sh"], work, "dataset/ already present")
        run([sys.executable, "code/evaluation/main.py"], work,
            "sample status 32/32")
        run([sys.executable, "scripts/check_claims.py"], work, "CLAIMS OK")
        run([sys.executable, "analysis/compare.py"], work, "status 32/32")
        run([sys.executable, "analysis/test_eval_negative.py"], work, "15/15")
        run([sys.executable, "analysis/test_intent.py"], work, "140/140")
        run([sys.executable, "analysis/activity_coverage.py"], work, "missed")

    payload = ZIP.read_bytes()
    print(f"PACKAGE OK  {ZIP.name}  {len(names)} files  {len(payload)} bytes")
    print(f"sha256 {hashlib.sha256(payload).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
