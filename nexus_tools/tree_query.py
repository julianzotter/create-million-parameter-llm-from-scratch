"""Read-only query cache over existing TREE/DIRLIST text files.

Reuses existing index lists (MUST-23, MUST-81) instead of creating a new
canonical index: the SQLite file is a DERIVED cache. Every hit keeps the
parent source file, its SHA-256 and the line number as locator (MUST-73),
so large tree lists never have to be sent to an LLM in full.

Usage:
    python -m nexus_tools.tree_query build cache.db TREE_A.txt TREE_B.txt
    python -m nexus_tools.tree_query search cache.db "SEILSTATIK" --limit 20
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

_SCHEMA = """
CREATE TABLE IF NOT EXISTS sources(
    source_path TEXT PRIMARY KEY, sha256 TEXT NOT NULL,
    size_bytes INTEGER NOT NULL, encoding TEXT NOT NULL, line_count INTEGER NOT NULL);
CREATE VIRTUAL TABLE IF NOT EXISTS lines USING fts5(
    text, source_path UNINDEXED, line_no UNINDEXED, tokenize='unicode61');
"""


def decode_bytes(raw: bytes) -> tuple[str, str]:
    """Decode Windows `tree`/`dir` exports (often UTF-16 with BOM, or cp850/cp1252)."""
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16"), "utf-16"
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw[3:].decode("utf-8"), "utf-8-sig"
    for enc in ("utf-8", "cp850", "cp1252"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1"), "latin-1"


def connect(db_path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(db_path)
    con.executescript(_SCHEMA)
    return con


def ingest(con: sqlite3.Connection, path: Path) -> dict[str, object]:
    """Add one tree file; unchanged files (same SHA-256) are skipped (delta instead of full rescan)."""
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    key = str(path)
    row = con.execute("SELECT sha256 FROM sources WHERE source_path=?", (key,)).fetchone()
    if row and row[0] == digest:
        return {"source_path": key, "sha256": digest, "action": "unchanged"}
    text, encoding = decode_bytes(raw)
    lines = text.splitlines()
    con.execute("DELETE FROM lines WHERE source_path=?", (key,))
    con.executemany(
        "INSERT INTO lines(text, source_path, line_no) VALUES (?,?,?)",
        ((ln.strip(), key, i) for i, ln in enumerate(lines, 1) if ln.strip()),
    )
    con.execute(
        "INSERT OR REPLACE INTO sources VALUES (?,?,?,?,?)",
        (key, digest, len(raw), encoding, len(lines)),
    )
    con.commit()
    return {"source_path": key, "sha256": digest, "encoding": encoding,
            "lines": len(lines), "action": "replaced" if row else "added"}


def _fts_query(term: str) -> str:
    """Quote each whitespace token so user input cannot inject FTS5 syntax."""
    tokens = [t.replace('"', '""') for t in term.split() if t]
    return " ".join(f'"{t}"' for t in tokens)


def search(con: sqlite3.Connection, term: str, limit: int = 20) -> list[dict[str, object]]:
    """Exact-token lookup with provenance; empty result means abstain (MUST-84)."""
    query = _fts_query(term)
    if not query:
        return []
    rows = con.execute(
        "SELECT l.text, l.source_path, l.line_no, s.sha256 FROM lines l "
        "JOIN sources s ON s.source_path = l.source_path "
        "WHERE lines MATCH ? ORDER BY l.source_path, l.line_no LIMIT ?",
        (query, limit),
    ).fetchall()
    return [
        {"text": t, "source_path": p, "locator": f"line {n}", "source_sha256": h}
        for t, p, n, h in rows
    ]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("db", type=Path)
    b.add_argument("files", type=Path, nargs="+")
    s = sub.add_parser("search")
    s.add_argument("db", type=Path)
    s.add_argument("term")
    s.add_argument("--limit", type=int, default=20)
    args = ap.parse_args(argv)
    con = connect(args.db)
    if args.cmd == "build":
        result: object = [ingest(con, f) for f in args.files]
    else:
        result = search(con, args.term, args.limit)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
