"""Shared loose-identifier scanner (stdlib only)."""
import json, re, unicodedata
from collections import defaultdict
from pathlib import Path

TEXT_EXT = {".json", ".ndjson", ".jsonl", ".csv", ".tsv", ".log", ".sql",
            ".txt", ".md", ".xml", ".yaml", ".yml", ".html"}
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d\-\s().]{7,}\d")
HASH_RE = re.compile(r"(?<![0-9A-Fa-f])[0-9A-Fa-f]{64}(?![0-9A-Fa-f])")
UID_RE = re.compile(r"(?<![A-Za-z0-9])(?:user|usr|u)[ _\-]?0*(\d+)(?![A-Za-z0-9])", re.I)


def email_key(s):
    s = unicodedata.normalize("NFKC", s).strip().lower()
    if "@" not in s:
        return s
    local, _, dom = s.rpartition("@")
    local = local.split("+", 1)[0].replace(".", "")
    return f"{local}@{dom}"


def phone_key(s):
    d = re.sub(r"\D", "", s)
    return d[-10:] if len(d) >= 10 else None


def hash_key(s):
    return s.strip().lower()


def uid_key(s):
    m = UID_RE.fullmatch(s.strip())
    return f"user_{int(m.group(1))}" if m else s.strip().lower()


KEYERS = {"email": email_key, "phone": phone_key, "hash": hash_key, "uid": uid_key}
FIELD = {"email": "emails", "phone": "phones", "hash": "hashes", "uid": "user_ids"}


class Index:
    def __init__(self, subjects_path):
        raw = json.loads(Path(subjects_path).read_text())
        self.case_subject = {c: v["subject"] for c, v in raw.items()}
        self.subject_cases = defaultdict(set)
        for c, s in self.case_subject.items():
            self.subject_cases[s].add(c)
        self.owner = defaultdict(set)
        self.exact = defaultdict(set)
        for v in raw.values():
            for kind, fld in FIELD.items():
                for tok in v.get(fld, []) or []:
                    k = KEYERS[kind](tok)
                    if k:
                        self.owner[(kind, k)].add(v["subject"])
                        self.exact[(kind, tok.strip().lower())].add(v["subject"])

    def tokens(self, line):
        for m in EMAIL_RE.finditer(line):
            yield "email", m.group(0)
        for m in HASH_RE.finditer(line):
            yield "hash", m.group(0)
        for m in PHONE_RE.finditer(line):
            yield "phone", m.group(0)
        for m in UID_RE.finditer(line):
            yield "uid", m.group(0)

    def resolve(self, kind, tok):
        k = KEYERS[kind](tok)
        out = []
        for s in self.owner.get((kind, k), ()):
            ex = s in self.exact.get((kind, tok.strip().lower()), ())
            out.append((s, "exact" if ex else "loose"))
        return out


def iter_files(root, ignore=None):
    ig = re.compile(ignore) if ignore else None
    root = Path(root)
    skipped = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = str(p.relative_to(root))
        if ig and ig.search(rel):
            continue
        if p.suffix.lower() in TEXT_EXT:
            yield rel, p
        else:
            skipped.append(rel)
    iter_files.skipped = skipped


def scan(index, root, ignore=None):
    for rel, p in iter_files(root, ignore):
        with open(p, "r", encoding="utf-8", errors="replace") as fh:
            for n, line in enumerate(fh, 1):
                hits = []
                for kind, tok in index.tokens(line):
                    for s, m in index.resolve(kind, tok):
                        hits.append((kind, tok, s, m))
                if hits:
                    yield rel, n, line, hits


def snippet(line, tok, w=70):
    i = line.find(tok)
    a = max(0, i - w)
    return line[a:i + len(tok) + w].strip().replace("\n", " ")
