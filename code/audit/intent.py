"""Authorization classifier for `request_text`.

A deletion audit is only meaningful when the person actually asked for
deletion. The corpus is multilingual and contains access, correction,
portability, marketing opt-out and login-support requests.

Design: deletion requires a delete directive (verb/noun stem in any supported
language) or an explicit "confirm it is gone" follow-up. A non-deletion marker
that governs the sentence (negated deletion, keep-the-account, opt-out,
copy/access, retraction) suppresses it. Conditional deletions stay deletions.
"""
from __future__ import annotations

import re
import unicodedata

DELETE = "DELETE"
NON_DELETE = "NON_DELETE"

# Substring stems, not whole words: covers imperative/infinitive/noun forms in
# the languages the corpus uses (EN, ES, PT, FR, DE, KO, JA).
_DELETE_TERMS = (
    # English
    "delet", "erase", "eras", "remov", "clos", "purge", "suppress",
    # Spanish
    "elimin", "elimín", "borr", "suprim", "cancel",
    # Portuguese
    "exclu", "apag", "cancel", "encerr",
    # French
    "supprim", "effac", "résili", "resili", "fermer", "fermez",
    # German
    "lösch", "loesch", "entfern", "kündig", "kuendig", "schließ", "schliess",
    # Korean
    "삭제", "지우", "제거", "폐쇄",
    # Japanese
    "削除", "消去", "閉鎖",
    # Chinese (not claimed, cheap coverage)
    "删除", "刪除",
)

# Markers that turn a sentence into a different privacy right.
_NON_DELETE_PATTERNS = (
    # English
    r"\bnot\b[^.]{0,50}\b(?:delet|eras|remov|clos|suppress)",
    r"\bnever\b[^.]{0,40}\b(?:asked|requested|wanted)\b[^.]{0,30}\b(?:delet|eras|remov)",
    r"\b(?:do not|don't|dont|please don't|please do not)\b[^.]{0,60}"
    r"\b(?:delet|eras|remov|clos|chang)",
    r"\bwithout\b[^.]{0,40}\b(?:remov|delet|eras|clos)",
    r"\b(?:keep|leave)\b[^.]{0,30}\b(?:the |my |this )?(?:account|profile)\b",
    r"\b(?:keep|leave)\b[^.]{0,20}\b(?:as it is|in place|active)\b",
    r"\b(?:still|continue to|continue)\s+(?:use|using|need|want)\b",
    r"\bmarketing\s+lists?\s+only\b",
    r"\bmailing\s+list\b",
    r"\b(?:stop|unsubscribe from)\b[^.]{0,30}\b(?:promotional|marketing|emails|mail)\b",
    r"\binformation request\b",
    r"\breset(?:ting)?\b[^.]{0,20}\blogin\b",
    r"\b(?:never mind|nevermind|cancel (?:that|the) request)\b",
    r"\bactually,?\s+keep\b",
    r"\bstop\b[^.]{0,30}\bdeleting\b",
    r"\bwhat\s+would\b[^.]{0,50}\b(?:delete|erase|remove)\b",
    r"\bwhat\s+happens\b[^.]{0,60}\b(?:delete|erase|remove|close)\b",
    r"\bexplain\b[^.]{0,40}\b(?:deletion|deleting)\b",
    r"\bqué\s+pasa\s+si\b[^.]{0,50}\b(?:elimin|borr)",
    r"\bo\s+que\s+acontece\s+se\b[^.]{0,50}\b(?:exclu|apag)",
    r"\bque\s+se\s+passe-t-il\s+si\b[^.]{0,50}\b(?:supprim|effac)",
    r"\bwas\s+passiert,?\s+wenn\b[^.]{0,50}\b(?:lösch|loesch)",
    r"(?:n'|ne\s+)effacez\s+rien",
    r"\bich\s+möchte\s+nicht\b[^.]{0,60}lösch",
    r"\bdas\s+ist\s+keine\b[^.]{0,40}löschung",
    r"삭제[^.]{0,25}원하지\s*않",
    r"\bif\s+i\s+asked\b",
    # Spanish
    r"\bno\s+(?:borren|borres|eliminen|elimines|supriman|apaguen|cancelen)\b",
    r"\bno\s+quiero\s+que\b[^.]{0,40}\b(?:eliminen|borren|supriman)\b",
    r"\bno\s+es\s+una\s+(?:solicitud|petición)\s+de\b",
    r"\bdejen\s+de\b[^.]{0,40}\b(?:eliminar|borrar)\b",
    r"\bsolo\s+quiero\b[^.]{0,50}\b(?:actualizar|corregir|cambiar)\b",
    # Portuguese
    r"\bnão\s+(?:excluam|apaguem|removam|eliminem)\b",
    r"\bnao\s+(?:excluam|apaguem|removam|eliminem)\b",
    r"\bnão\s+quero\s+que\b[^.]{0,40}\b(?:excluam|apaguem)\b",
    r"\bnão\s+é\s+um\s+pedido\s+de\b",
    r"\bparem\s+de\b[^.]{0,40}\b(?:excluir|apagar)\b",
    r"\bsó\s+quero\b[^.]{0,50}\b(?:atualizar|corrigir|alterar)\b",
    # French
    r"\bne\s+(?:supprimez|supprimer|effacez)\s+pas\b",
    r"\bne\s+pas\s+(?:supprimer|effacer)\b",
    r"\bje\s+ne\s+veux\s+pas\b[^.]{0,40}\b(?:supprim|effac)",
    r"\bce\s+n'est\s+pas\s+une\s+demande\s+de\b",
    r"\barrêtez\s+de\b[^.]{0,40}\b(?:supprimer|effacer)\b",
    r"\b(?:garder|gardez)\b[^.]{0,30}\b(?:le\s+compte|mon\s+compte)\b",
    r"\bseulement\b[^.]{0,50}\b(?:changer|corriger|modifier)\b",
    # German
    r"\bnicht\s+löschen\b",
    r"\bnicht\s+loeschen\b",
    r"\blöschen\s+sie\s+nichts\b",
    r"\bich\s+möchte\s+nicht\b[^.]{0,40}\b(?:löschen|loeschen)\b",
    r"\bdas\s+ist\s+keine\b[^.]{0,30}\b(?:löschung|loeschung)\b",
    r"\bhören\s+sie\s+auf\b[^.]{0,40}\b(?:löschen|loeschen)\b",
    r"\b(?:behalten|behalte)\b[^.]{0,30}\bkonto\b",
    r"\bnur\b[^.]{0,50}\b(?:ändern|korrigieren)\b",
    # Korean
    r"삭제하지\s*마",
    r"삭제하지\s*않",
    r"삭제를?\s*원하지\s*않",
    r"삭제\s*요청이\s*아니",
    r"삭제하면\s*어떻게",
    r"유지해\s*주",
    r"삭제하지\s*말",
    # Japanese
    r"削除しないで",
    r"削除しない",
    r"削除を希望しません",
    r"削除依頼ではなく",
    r"削除するとどう",
    r"残して",
)

_KEEP_PATTERNS = (
    r"\b(?:keep|leave)\b[^.]{0,30}\b(?:the |my |this )?(?:account|profile)\b",
    r"\b(?:keep|leave)\b[^.]{0,20}\b(?:as it is|in place|active)\b",
    r"\b(?:garder|gardez)\b[^.]{0,30}\b(?:le\s+compte|mon\s+compte)\b",
    r"\b(?:behalten|behalte)\b[^.]{0,30}\bkonto\b",
)
_COMPILED_KEEP = tuple(re.compile(p, re.IGNORECASE) for p in _KEEP_PATTERNS)
_COMPILED_NON_DELETE = tuple(re.compile(p, re.IGNORECASE) for p in _NON_DELETE_PATTERNS)

# Follow-ups that audit an already-requested deletion without repeating the verb.
_IMPLICIT_DELETE_PATTERNS = (
    r"\bconfirm\b[^.]{0,60}\b(?:gone|removed|deleted|erased|absent|no longer)",
    r"\bverify\b[^.]{0,60}\b(?:gone|removed|deleted|erased|absent|no longer)",
    r"\bprofile\s+is\s+gone\b",
    r"\baccount\s+(?:still\s+exists|existed)\b",
    r"\bshould\s+(?:already\s+)?be\s+(?:gone|deleted|removed)\b",
    r"\bconfirma\b[^.]{0,60}\b(?:no\s+existe|borrad|eliminad)",
    r"\bconfirme\b[^.]{0,60}\b(?:não\s+existe|nao\s+existe|apagad|excluíd)",
    r"\bconfirmez\b[^.]{0,60}\b(?:n'existe|supprim|effac)",
    r"\bbestätigen\s+sie\b[^.]{0,60}\b(?:nicht\s+mehr\s+existiert|gelöscht)",
    r"존재하지\s*않는지\s*확인",
    r"이미\s*삭제되었어야",
    r"存在しないことを確認",
    r"すでに削除されているはず",
)
_COMPILED_IMPLICIT = tuple(re.compile(p, re.IGNORECASE) for p in _IMPLICIT_DELETE_PATTERNS)

# "if you cannot keep it, delete it" — conditional deletion beats the
# keep-the-account marker.
_CONDITIONAL = re.compile(
    r"\b(?:if|si|se|wenn)\b[^.]{0,80}\b(?:delet|eras|remov|elimin|borr|exclu|apag|supprim|"
    r"lösch|loesch)",
    re.IGNORECASE,
)


def _normalise(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    return re.sub(r"\s+", " ", text).strip()


def classify(request_text: str) -> tuple[str, str]:
    """Return (verdict, reason). Deterministic and side-effect free."""
    text = _normalise(request_text)
    lowered = text.lower()
    non_delete_hits = [p.pattern for p in _COMPILED_NON_DELETE if p.search(lowered)]
    keep_hits = [p.pattern for p in _COMPILED_KEEP if p.search(lowered)]
    has_delete = any(term in lowered for term in _DELETE_TERMS)
    implicit = any(p.search(lowered) for p in _COMPILED_IMPLICIT)

    # A conditional deletion ("if you cannot keep it, delete it") only
    # overrides keep-the-account phrasing, never a negation or a hypothetical.
    if non_delete_hits:
        only_keep = all(hit in keep_hits for hit in non_delete_hits)
        if not (only_keep and _CONDITIONAL.search(lowered)):
            return NON_DELETE, f"non-deletion intent: {len(non_delete_hits)} marker(s)"
    if has_delete:
        return DELETE, "deletion directive"
    if implicit:
        return DELETE, "implicit deletion context"
    return NON_DELETE, "no deletion directive"
