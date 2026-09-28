"""Read-only duplicate-candidate scanner (Baseline MUST-157).

Input: JSON list of file metadata, e.g. exported from a Drive listing:
    [{"id": "...", "title": "...", "size": 123 | "123", "md5"?: "...", "mimeType"?: "..."}]

Every finding is a DUPLICATE_CANDIDATE (MUST-157); `basis` states the evidence,
strongest first: content_hash > title_size > size_only. A file pair is reported
once, under its strongest basis.

Not compared / excluded:
- Drive shortcuts; entries without id (listed under "skipped")
- files without a usable size or hash (e.g. native Google Docs/Sheets) and size 0
- size_only pairs whose titles share a stem after removing version suffixes
  (v1.0, V2, -v1.1) and IN/OUT markers: legitimate version / IN-OUT pairs
The scanner never allocates IDs, renames, moves or deletes anything.
"""
from __future__ import annotations

import itertools
import json
import re
import sys
from collections import defaultdict
from collections.abc import Callable, Hashable
from pathlib import Path
from typing import Any

SHORTCUT_MIME = "application/vnd.google-apps.shortcut"
_VERSION = re.compile(r"(?i)[ _.-]v\d+(\.\d+)*")
_INOUT = re.compile(r"(?i)(^|[ _.-])(in|out)(?=$|[ _.-])")
_BASES = ("content_hash", "title_size", "size_only")

FileMeta = dict[str, Any]


def _size(f: FileMeta) -> int | None:
    try:
        n = int(str(f.get("size")).strip())
    except (TypeError, ValueError):
        return None
    return n if n > 0 else None


def _stem(title: str | None) -> str:
    base = (title or "").rsplit(".", 1)[0]
    return _INOUT.sub(r"\1", _VERSION.sub("", base)).strip(" _.-").lower()


def _keys() -> dict[str, Callable[[FileMeta], Hashable | None]]:
    return {
        "content_hash": lambda f: f.get("sha256") or f.get("md5"),
        "title_size": lambda f: (f["title"], _size(f)) if f.get("title") and _size(f) else None,
        "size_only": _size,
    }


def scan(files: list[FileMeta]) -> dict[str, Any]:
    """Return {"findings": [...], "skipped": [...], "not_comparable": n}."""
    skipped = [f for f in files if not f.get("id")]
    real = [f for f in files if f.get("id") and f.get("mimeType") != SHORTCUT_MIME]
    reported: set[frozenset[str]] = set()
    findings: list[dict[str, Any]] = []
    keys = _keys()
    for basis in _BASES:
        buckets: dict[Hashable, list[FileMeta]] = defaultdict(list)
        for f in real:
            k = keys[basis](f)
            if k is not None:
                buckets[k].append(f)
        for group in buckets.values():
            for a, b in itertools.combinations(group, 2):
                pair = frozenset((a["id"], b["id"]))
                if pair in reported or a["id"] == b["id"]:
                    continue
                if basis == "size_only" and _stem(a.get("title")) == _stem(b.get("title")):
                    continue
                reported.add(pair)
                findings.append(_finding(basis, a, b))
    not_comparable = sum(1 for f in real if keys["content_hash"](f) is None and _size(f) is None)
    return {"findings": findings, "skipped": skipped, "not_comparable": not_comparable}


def _finding(basis: str, a: FileMeta, b: FileMeta) -> dict[str, Any]:
    return {
        "classification": "DUPLICATE_CANDIDATE",
        "basis": basis,
        "strength": {"content_hash": "strong", "title_size": "medium", "size_only": "weak"}[basis],
        "files": [{k: f.get(k) for k in ("id", "title", "size", "parent")} for f in (a, b)],
        "action": "NONE (read-only); registry owner decides identity/status",
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
