"""Markdown vault ingest and lint helpers."""

from __future__ import annotations

import json
import re
from dataclasses import asdict
from pathlib import Path

from .models import VaultDoc, VaultIndex, VaultIssue

WIKI_LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
TAG_RE = re.compile(r"(?<!\w)#([A-Za-z0-9_-]+)")
WORD_RE = re.compile(r"[\wА-Яа-яЁё]+", re.UNICODE)
ABSOLUTE_LOCAL_PATH_RE = re.compile(
    r"(?:/Users/[A-Za-z0-9_.-]+|/home/[A-Za-z0-9_.-]+|[A-Za-z]:\\Users\\[^\\\s]+)"
)
SKIP_DIRS = {".git", ".hg", ".svn", "__pycache__", "node_modules", ".talk-private", "local"}


def iter_markdown_files(root: Path) -> list[Path]:
    """Return markdown files under root in deterministic order."""
    root = root.resolve()
    paths: list[Path] = []
    for path in root.rglob("*.md"):
        rel_parts = path.relative_to(root).parts
        if any(part in SKIP_DIRS or part.startswith(".") for part in rel_parts[:-1]):
            continue
        paths.append(path)
    return sorted(paths, key=lambda p: p.relative_to(root).as_posix())


def _extract_title(markdown: str, fallback: str) -> tuple[str, bool]:
    for line in markdown.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            if title:
                return title, True
    return fallback, False


def _extract_links(markdown: str) -> list[str]:
    return sorted({match.strip() for match in WIKI_LINK_RE.findall(markdown) if match.strip()})


def _extract_tags(markdown: str) -> list[str]:
    return sorted({match.strip() for match in TAG_RE.findall(markdown) if match.strip()})


def read_doc(root: Path, path: Path) -> VaultDoc:
    markdown = path.read_text(encoding="utf-8")
    rel = path.relative_to(root).as_posix()
    title, has_h1 = _extract_title(markdown, path.stem.replace("-", " ").title())
    return VaultDoc(
        path=rel,
        title=title,
        links=_extract_links(markdown),
        tags=_extract_tags(markdown),
        word_count=len(WORD_RE.findall(markdown)),
        has_h1=has_h1,
    )


def build_index(root: Path) -> VaultIndex:
    root = root.resolve()
    docs = [read_doc(root, path) for path in iter_markdown_files(root)]
    return VaultIndex(root=root.as_posix(), docs=docs)


def write_index(index: VaultIndex, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(index.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def load_index(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def lint_vault(root: Path) -> list[VaultIssue]:
    root = root.resolve()
    docs = [read_doc(root, path) for path in iter_markdown_files(root)]
    issues: list[VaultIssue] = []

    title_to_paths: dict[str, list[str]] = {}
    resolvable_links: set[str] = set()
    for doc in docs:
        title_to_paths.setdefault(doc.title, []).append(doc.path)
        resolvable_links.add(doc.title)
        resolvable_links.add(Path(doc.path).stem)

    for doc in docs:
        if not doc.has_h1:
            issues.append(
                VaultIssue(
                    code="missing-h1",
                    path=doc.path,
                    message="note has no H1 title",
                )
            )

        text = (root / doc.path).read_text(encoding="utf-8")
        body_lines = [line for line in text.splitlines() if not line.startswith("# ")]
        if not " ".join(body_lines).strip():
            issues.append(
                VaultIssue(
                    code="empty-body",
                    path=doc.path,
                    message="note body is empty",
                    severity="warning",
                )
            )

        if ABSOLUTE_LOCAL_PATH_RE.search(text):
            issues.append(
                VaultIssue(
                    code="absolute-local-path",
                    path=doc.path,
                    message="note contains a local absolute path; redact or replace with a placeholder",
                )
            )

        for link in doc.links:
            if link not in resolvable_links:
                issues.append(
                    VaultIssue(
                        code="unresolved-link",
                        path=doc.path,
                        message=f"[[{link}]] is not present in this vault",
                    )
                )

    for title, paths in sorted(title_to_paths.items()):
        if len(paths) > 1:
            canonical = _choose_canonical_title_path(title, paths)
            for path in paths:
                if path == canonical:
                    continue
                issues.append(
                    VaultIssue(
                        code="duplicate-title",
                        path=path,
                        message=f"title duplicates {canonical}: {title}",
                    )
                )

    return sorted(issues, key=lambda issue: (issue.path, issue.code, issue.message))


def _choose_canonical_title_path(title: str, paths: list[str]) -> str:
    """Choose a stable canonical note for duplicate-title reporting."""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    for path in sorted(paths):
        if Path(path).stem == slug:
            return path
    return sorted(paths)[0]


def issues_to_json(issues: list[VaultIssue]) -> str:
    return json.dumps([asdict(issue) for issue in issues], ensure_ascii=False, indent=2, sort_keys=True)
