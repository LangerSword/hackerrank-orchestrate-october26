"""Authorization classifier for `request_text`.

A deletion audit is only meaningful when the person actually asked for
deletion.  The corpus is multilingual and deliberately contains access,
correction, portability, marketing opt-out and login-support requests.

The classifier is deliberately conservative: it requires a deletion directive
and rejects the request when a non-deletion marker governs the sentence.
"""
from __future__ import annotations

import re
import unicodedata

DELETE = "DELETE"
NON_DELETE = "NON_DELETE"

# Multilingual deletion directives.  Substring matching (not \b) so CJK works.
_DELETE_TERMS = (
    "delete", "deleting", "deleted", "deletion", "erase", "erasure", "remov",
    "close my account", "close this account", "close the account", "closing", "closed my account",
    "purge",
    "eliminar", "eliminación", "eliminacion", "excluir", "exclusão", "exclusao",
    "apagar", "borrar", "remover", "cancelar la cuenta",
    "supprimer", "suppression", "effacer", "résiliation", "resilier",
    "löschen", "loeschen", "kündigen", "kuendigen", "entfernen",
    "削除", "삭제", "删除", "刪除", "удал", "حذف", "verwijder", "usuń", "usun",
)

# Markers that turn a sentence into a different privacy right.
_NON_DELETE_PATTERNS = (
    r"\bnot\b[^.]{0,50}\b(?:delet|eras|remov|clos|suppress)",
    r"\bnever\b[^.]{0,40}\b(?:asked|requested|wanted)\b[^.]{0,30}\b(?:delet|eras|remov)",
    r"\bnot\s+(?:a|an)\s+(?:request|deletion)",
    r"\b(?:do not|don't|dont|please don't|please do not)\b[^.]{0,60}"
    r"\b(?:delet|eras|remov|clos|chang)",
    r"\bwithout\b[^.]{0,40}\b(?:remov|delet|eras|clos)",
    r"\b(?:keep|leave)\b[^.]{0,40}\b(?:account|profile|history|as it is|in place|active)",
    r"\b(?:still|continue to|continue)\s+(?:use|using|need|want)\b",
    r"\bmarketing\s+lists?\s+only\b",
    r"\b(?:stop|unsubscribe from)\b[^.]{0,30}\b(?:promotional|marketing|emails)\b",
    r"\binformation request\b",
    r"\breset(?:ting)?\b[^.]{0,20}\blogin\b",
)

_COMPILED_NON_DELETE = tuple(re.compile(p, re.IGNORECASE) for p in _NON_DELETE_PATTERNS)


def _normalise(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    return re.sub(r"\s+", " ", text).strip()


def classify(request_text: str) -> tuple[str, str]:
    """Return (verdict, reason).  Deterministic and side-effect free."""
    text = _normalise(request_text)
    lowered = text.lower()
    non_delete_hits = [p.pattern for p in _COMPILED_NON_DELETE if p.search(lowered)]
    if non_delete_hits:
        # "not asking for deletion", "leave the account active", "copy of my
        # invoices" and similar markers describe another privacy right.
        return NON_DELETE, f"non-deletion intent: {len(non_delete_hits)} marker(s)"
    has_delete = any(term in lowered for term in _DELETE_TERMS)
    # Some audited cases are follow-ups ("please confirm the profile is gone")
    # that do not repeat the word delete; the surrounding record is an
    # authorized deletion request, so deletion is the default when no
    # non-deletion marker governs the text.
    return DELETE, ("deletion directive" if has_delete else "implicit deletion context")
