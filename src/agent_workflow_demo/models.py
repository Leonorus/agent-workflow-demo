"""Data models for the vault demo."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal


@dataclass(frozen=True)
class VaultDoc:
    path: str
    title: str
    links: list[str]
    tags: list[str]
    word_count: int
    has_h1: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class VaultIndex:
    root: str
    docs: list[VaultDoc]

    def to_dict(self) -> dict[str, object]:
        return {"root": self.root, "docs": [doc.to_dict() for doc in self.docs]}


@dataclass(frozen=True)
class VaultIssue:
    code: str
    path: str
    message: str
    severity: Literal["error", "warning"] = "error"

    def to_line(self) -> str:
        return f"{self.severity.upper()} {self.path} {self.code}: {self.message}"
