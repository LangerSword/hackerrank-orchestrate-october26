#!/usr/bin/env python3
"""Build or verify the document digest.

The digest is a content-addressed cache of *facts* read from PDFs and console
screenshots. It never contains verdicts, labels, or case ids.

    python3 code/tools/build_document_digest.py --text     # print extracted text
    python3 code/tools/build_document_digest.py --hashes   # rewrite sha256 map
    python3 code/tools/build_document_digest.py --check    # verify cache freshness

`--hashes` records the SHA-256 of every PDF/PNG in `dataset/evidence_files.csv`
into `_meta.content_sha256`. At runtime the index hashes each artefact and only
uses a digest entry when the hash matches, so editing an artefact invalidates
its cached facts instead of silently reusing them.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "dataset"
DIGEST = ROOT / "code" / "audit" / "digests" / "documents.json"


def extract(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf" and shutil.which("pdftotext"):
        return subprocess.run(["pdftotext", "-layout", str(path), "-"],
                              capture_output=True, text=True, timeout=60).stdout
    if suffix in {".png", ".jpg", ".jpeg"} and shutil.which("tesseract"):
        return subprocess.run(["tesseract", str(path), "-", "--psm", "6"],
                              capture_output=True, text=True, timeout=120).stdout
    return path.read_text(encoding="utf-8", errors="replace")


def artifacts() -> list[dict]:
    with (DATASET / "evidence_files.csv").open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle)
                if row["file_path"].lower().endswith((".pdf", ".png", ".jpg", ".jpeg"))]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", action="store_true", help="print extracted text per artefact")
    parser.add_argument("--hashes", action="store_true", help="write content_sha256 into the digest")
    parser.add_argument("--check", action="store_true", help="verify every digest entry matches a file hash")
    args = parser.parse_args()

    rows = artifacts()
    if args.hashes:
        digest = json.loads(DIGEST.read_text()) if DIGEST.exists() else {"_meta": {}}
        digest.setdefault("_meta", {})["content_sha256"] = {
            hashlib.sha256((DATASET / row["file_path"]).read_bytes()).hexdigest(): row["file_id"]
            for row in rows
        }
        digest["_meta"]["note"] = (
            "Facts transcribed from participant-facing PDFs and console screenshots. "
            "Entries are keyed by content hash in _meta.content_sha256; a changed "
            "artefact invalidates its entry. Regenerate with --text and re-verify."
        )
        DIGEST.write_text(json.dumps(digest, indent=2) + "\n")
        print(f"wrote {len(rows)} content hashes to {DIGEST}")
        return 0

    digest = json.loads(DIGEST.read_text())
    hashes = digest.get("_meta", {}).get("content_sha256", {})
    missing = []
    for row in rows:
        path = DATASET / row["file_path"]
        digest_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if hashes.get(digest_hash) != row["file_id"]:
            missing.append(row["file_id"])
        if args.text:
            print(f"\n### {row['file_id']} {row['file_path']} {row['captured_at']}")
            print(extract(path)[:4000])
    if args.check:
        print("all digest entries match file hashes" if not missing
              else f"stale or unhashed artefacts: {missing}")
        return 0 if not missing else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
