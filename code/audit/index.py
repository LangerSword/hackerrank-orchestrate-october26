"""Evidence index: load the manifest, parse every artefact once, and resolve
which subject each observation belongs to.
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from .evidence import (
    EvidenceFile,
    _parse_digest,
    _parse_handover,
    _parse_json,
    _parse_logs,
    _parse_sql,
)
from .model import Fact, parse_ts
from .tables import IdentityGraph


class EvidenceIndex:
    def __init__(self) -> None:
        self.files: dict[str, EvidenceFile] = {}
        self.facts: list[Fact] = []
        self.empty_snapshots: list[dict] = []
        self.resource_users: dict[tuple[str, str], set[str]] = defaultdict(set)
        self.user_facts: dict[str, list[Fact]] = defaultdict(list)
        self.unattributed: list[Fact] = []

    # ------------------------------------------------------------------ load
    @classmethod
    def load(cls, dataset_dir: Path, identities: IdentityGraph,
             digest_path: Path | None = None) -> "EvidenceIndex":
        index = cls()
        digest = {}
        if digest_path and digest_path.exists():
            digest = json.loads(digest_path.read_text())
        index._dataset_dir = dataset_dir
        manifest = dataset_dir / "evidence_files.csv"
        with manifest.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            path = dataset_dir / row["file_path"]
            evidence = EvidenceFile(
                file_id=row["file_id"],
                path=path,
                origin=row["origin"],
                captured_at=parse_ts(row["captured_at"]),
            )
            index.files[evidence.file_id] = evidence
            facts, empties = index._extract(evidence, digest)
            index.facts.extend(facts)
            index.empty_snapshots.extend(empties)

        index._seed_activity_links(identities)
        index._attribute(identities)
        return index

    def _seed_activity_links(self, identities: IdentityGraph) -> None:
        """Data-catalog links are identity evidence in their own right."""
        path = self._dataset_dir / "system_activity.csv"
        if not path.exists():
            return
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                if row.get("event_type") not in {"LINK_RESOURCE_IDENTITY", "CLASSIFY_REQUEST"}:
                    continue
                user_id = row.get("details", "").strip()
                match = re.search(r"\b(user_\d+)\b", user_id)
                if not match:
                    continue
                system = row.get("target_system", "").strip()
                resource = row.get("resource_id", "").strip()
                if system and resource:
                    self.resource_users[(system, resource)].add(match.group(1))

    def _extract(self, evidence: EvidenceFile, digest: dict):
        suffix = evidence.path.suffix.lower()
        if evidence.file_id in digest:
            return _parse_digest(evidence, digest), []
        text = ""
        if suffix in {".json", ".sql", ".log", ".txt"}:
            text = evidence.path.read_text(encoding="utf-8", errors="replace")
        elif suffix == ".pdf":
            text = self._pdf_text(evidence.path)
        elif suffix in {".png", ".jpg", ".jpeg"}:
            text = self._ocr_text(evidence.path)
        else:
            return [], []

        if suffix == ".json":
            return _parse_json(evidence, text)
        if suffix == ".sql":
            return _parse_sql(evidence, text), []
        if suffix == ".log":
            return _parse_logs(evidence, text), []
        if suffix == ".txt":
            facts, empties = _parse_handover(evidence, text), []
            # Handover notes list point-in-time states for many subjects; they
            # are parsed by the dedicated reader only.
            return facts, empties
        # PDF / screenshot without a digest: keep the text for the debug tool
        # but do not invent facts from free text at runtime.
        return [], []

    @staticmethod
    def _pdf_text(path: Path) -> str:
        if not shutil.which("pdftotext"):
            return ""
        result = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                                capture_output=True, text=True, timeout=60)
        return result.stdout

    @staticmethod
    def _ocr_text(path: Path) -> str:
        if not shutil.which("tesseract"):
            return ""
        result = subprocess.run(["tesseract", str(path), "-", "--psm", "6"],
                                capture_output=True, text=True, timeout=120)
        return result.stdout

    # ------------------------------------------------------------- attribute
    def _attribute(self, identities: IdentityGraph) -> None:
        # Pass 1: facts carrying direct identifiers establish resource owners.
        for fact in self.facts:
            users = set()
            for key in fact.identity_keys():
                user = identities.resolve_identifier(key)
                if user:
                    users.add(user)
            if users:
                for user in users:
                    self.resource_users[(fact.system, fact.resource_id)].add(user)
                fact.detail.setdefault("users", sorted(users))
        # Pass 2: anonymous observations inherit the owner from the resource
        # index built above (a resource keeps one owner in this dataset).
        for fact in self.facts:
            users = set(fact.detail.get("users", []))
            if not users:
                users = self.resource_users.get((fact.system, fact.resource_id), set())
            if users:
                fact.detail["users"] = sorted(users)
                for user in users:
                    self.user_facts[user].append(fact)
            else:
                self.unattributed.append(fact)

    # ---------------------------------------------------------------- access
    def facts_for(self, user_id: str, cutoff: datetime) -> list[Fact]:
        return [f for f in self.user_facts.get(user_id, []) if f.observed_at <= cutoff]

    def evidence_files_for(self, facts: list[Fact]) -> set[str]:
        return {f.file_id for f in facts}

    def captured_before(self, file_id: str, cutoff: datetime) -> bool:
        evidence = self.files.get(file_id)
        return bool(evidence and evidence.captured_at <= cutoff)
