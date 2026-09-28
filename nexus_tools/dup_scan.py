"""Read-only duplicate-candidate scanner (Baseline MUST-157).

Input: JSON list of file metadata, e.g. exported from a Drive listing:
    [{"id": "...", "title": "...", "size": 123, "md5": "..."?, "parent": "..."?}]

Rules:
- same title + same size  -> DUPLICATE_CANDIDATE (never proven identity)
- same content hash       -> CONTENT_HASH_MATCH (strong hint; registry decides)
- Drive shortcuts, IN/OUT pairs and version pairs (v1.0 vs v1.1) are not grouped
- the scanner never allocates IDs, never renames, moves or deletes anything
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

SHORTCUT_MIME = "application/vnd.google-apps.shortcut"


def _hash_of(f: dict[str, Any]) -> str | None:
    return f.get("sha256") or f.get("md5")


def _groups(files: list[dict[str, Any]], key) -> list[list[dict[str, Any]]]:
    buckets: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for f in files:
        k = key(f)
        if k is not None:
            buckets[k].append(f)
    return [g for g in buckets.values() if len(g) > 1]


def _versioned_title(title: str) -> bool:
    return bool(re.search(r"_v\d+\.\d+", title))


def scan(files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return candidate groups; each group lists file IDs and the evidence used."""
    real = [f for f in files if f.get("mimeType") != SHORTCUT_MIME]
    findings: list[dict[str, Any]] = []
    seen: set[frozenset[str]] = set()
    for g in _groups(real, lambda f: _hash_of(f)):
        ids = frozenset(f["id"] for f in g)
        seen.add(ids)
        findings.append(_finding("CONTENT_HASH_MATCH", g, "equal content hash"))
    for g in _groups(real, lambda f: (f.get("title"), f.get("size")) if f.get("size") else None):
        ids = frozenset(f["id"] for f in g)
        if ids in seen:
            continue
        findings.append(_finding("DUPLICATE_CANDIDATE", g, "same title and size"))
    for g in _groups(real, lambda f: f.get("size") if f.get("size") and int(f["size"]) > 1024 else None):
        ids = frozenset(f["id"] for f in g)
        titles = {f.get("title") for f in g}
        if ids in seen or len(titles) == 1 or any(_versioned_title(t or "") for t in titles):
            continue
        seen.add(ids)
        findings.append(_finding("SIZE_ONLY_HINT", g, "same size, different title (weak)"))
    return findings


def _finding(kind: str, group: list[dict[str, Any]], basis: str) -> dict[str, Any]:
    return {
        "classification": kind,
        "basis": basis,
        "files": [{k: f.get(k) for k in ("id", "title", "size", "parent")} for f in group],
        "action": "NONE (read-only); registry owner decides CANONICAL/REFERENCE/DERIVED",
    }


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print("usage: python -m nexus_tools.dup_scan listing.json", file=sys.stderr)
        return 2
    files = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    json.dump(scan(files), sys.stdout, ensure_ascii=False, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
