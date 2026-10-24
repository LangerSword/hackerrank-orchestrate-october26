"""CSV table ingestion and the identity graph.

`user_identities.csv` only holds the *current* identity.  `user_audit_log.csv`
holds every field transition, so the historical email/phone/hash chain has to
be rebuilt before any evidence can be attributed.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from .model import (
    Case,
    Identity,
    UserIdentity,
    norm_email,
    norm_hash,
    norm_phone,
    parse_ts,
)


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_cases(dataset_dir: Path, name: str = "deletion_requests.csv") -> list[Case]:
    cases = []
    for row in read_rows(dataset_dir / name):
        cases.append(
            Case(
                case_id=row["case_id"].strip(),
                email=row["email"].strip(),
                requested_at=parse_ts(row["requested_at"]),
                reported_status=row["reported_status"].strip(),
                reported_at=parse_ts(row["reported_at"]),
                audit_at=parse_ts(row["audit_at"]),
                request_text=row["request_text"],
            )
        )
    return cases


def load_identities(dataset_dir: Path) -> list[Identity]:
    out = []
    for row in read_rows(dataset_dir / "user_identities.csv"):
        out.append(
            Identity(
                user_id=row["user_id"].strip(),
                name=row["name"].strip(),
                email=row["email"].strip(),
                phone=row["phone"].strip(),
                email_hash=row["email_hash"].strip(),
                updated_at=parse_ts(row["updated_at"]),
            )
        )
    return out


class IdentityGraph:
    """Resolves any identifier (current or historical) to one subject."""

    def __init__(self) -> None:
        self.users: dict[str, UserIdentity] = {}
        self.email_to_user: dict[str, str] = {}
        self.hash_to_user: dict[str, str] = {}
        self.phone_to_user: dict[str, str] = {}
        self.name_to_users: dict[str, set[str]] = defaultdict(set)

    # ------------------------------------------------------------- building
    @classmethod
    def build(cls, dataset_dir: Path) -> "IdentityGraph":
        graph = cls()
        for identity in load_identities(dataset_dir):
            user = graph.users.setdefault(
                identity.user_id, UserIdentity(user_id=identity.user_id)
            )
            graph._add_email(user, identity.email)
            graph._add_hash(user, identity.email_hash)
            graph._add_phone(user, identity.phone)
            graph._add_name(user, identity.name)

        for row in read_rows(dataset_dir / "user_audit_log.csv"):
            user_id = row["user_id"].strip()
            user = graph.users.setdefault(user_id, UserIdentity(user_id=user_id))
            field = row["field_name"].strip().lower()
            new_value = row["new_value"].strip()
            old_value = row["old_value"].strip()
            if field == "email":
                graph._add_email(user, new_value)
                graph._add_email(user, old_value)
            elif field == "email_hash":
                graph._add_hash(user, new_value)
                graph._add_hash(user, old_value)
            elif field == "phone":
                graph._add_phone(user, new_value)
                graph._add_phone(user, old_value)
            elif field == "name":
                graph._add_name(user, new_value)
                graph._add_name(user, old_value)
        return graph

    def _add_email(self, user: UserIdentity, value: str) -> None:
        email = norm_email(value)
        if not email or "@" not in email:
            return
        user.emails.add(email)
        # First writer wins: an address is never shared in this dataset, and
        # refusing to overwrite keeps a stale audit row from stealing a
        # current identity.
        self.email_to_user.setdefault(email, user.user_id)

    def _add_hash(self, user: UserIdentity, value: str) -> None:
        digest = norm_hash(value)
        if not digest:
            return
        user.hashes.add(digest)
        self.hash_to_user.setdefault(digest, user.user_id)

    def _add_phone(self, user: UserIdentity, value: str) -> None:
        phone = norm_phone(value)
        if len(phone) < 7:
            return
        user.phones.add(phone)
        self.phone_to_user.setdefault(phone, user.user_id)

    def _add_name(self, user: UserIdentity, value: str) -> None:
        name = (value or "").strip().lower()
        if not name:
            return
        user.names.add(name)
        self.name_to_users[name].add(user.user_id)

    # ------------------------------------------------------------- lookup
    def resolve_email(self, email: str) -> str:
        return self.email_to_user.get(norm_email(email), "")

    def resolve_identifier(self, value: str) -> str:
        """Best-effort resolution for one raw identifier string."""
        value = (value or "").strip()
        if not value:
            return ""
        lowered = value.lower()
        if lowered.startswith("p:") and lowered[2:] in self.phone_to_user:
            return self.phone_to_user[lowered[2:]]
        if lowered in self.email_to_user:
            return self.email_to_user[lowered]
        if lowered in self.hash_to_user:
            return self.hash_to_user[lowered]
        if lowered.startswith("user_") and lowered in self.users:
            return lowered
        digits = norm_phone(value)
        if len(digits) >= 7 and digits in self.phone_to_user:
            return self.phone_to_user[digits]
        return ""

    def resolve_many(self, values) -> set[str]:
        out = set()
        for value in values:
            user = self.resolve_identifier(value)
            if user:
                out.add(user)
        return out

    def identifiers_for(self, user_id: str) -> set[str]:
        user = self.users.get(user_id)
        return user.identifiers() if user else {user_id.lower()}

    def owned_identifiers(self, user_id: str) -> list[str]:
        """Concrete values an evidence file can contain, longest first."""
        user = self.users.get(user_id)
        if not user:
            return [user_id.lower()]
        values = sorted(user.emails, key=len, reverse=True)
        values += [h for h in sorted(user.hashes, key=len, reverse=True) if h]
        values += [p for p in sorted(user.phones, key=len, reverse=True) if p]
        values.append(user_id.lower())
        return values
