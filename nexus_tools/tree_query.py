"""Read-only query cache over existing TREE/DIRLIST text files.

Reuses existing index lists (MUST-23, MUST-81) instead of creating a new
canonical index: the SQLite file is a DERIVED, rebuildable cache. Every hit
keeps the parent source file, its SHA-256 and the line number as locator
(MUST-73), so large tree lists never have to be sent to an LLM in full.

Search is exact-token (FTS5 unicode61), not prefix: "SEIL" does not match
"SEILSTATIK". No hit means abstain (MUST-84), not "does not exist".

Usage:
    python -m nexus_tools.tree_query build cache.db TREE_A.txt [--encoding cp850]
    python -m nexus_tools.tree_query search cache.db "SEILSTATIK" [--limit 20] [--verify]
    python -m nexus_tools.tree_query prune cache.db
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
    source_path TEXT PRIMARY KEY, sha256 TEXT NOT NULL, size_bytes INTEGER NOT NULL,
    encoding TEXT NOT NULL, encoding_basis TEXT NOT NULL, line_count INTEGER NOT NULL);
CREATE VIRTUAL TABLE IF NOT EXISTS lines USING fts5(
    text, source_path UNINDEXED, line_no UNINDEXED, tokenize='unicode61');
"""
MAX_LIMIT = 1000
_CP850_BOX = (b"\xc4\xc4", b"\xb3", b"\xc3\xc4", b"\xc0\xc4")  # ── │ ├─ └─ in cp850


def _nul_utf16(raw: bytes) -> str | None:
    """Detect BOM-less UTF-16 by the share of NUL bytes on odd/even positions."""
    sample = raw[:4096]
    half = len(sample) // 2
    if half < 2:
        return None
    odd = sample[1::2].count(0) / half
    even = sample[0::2].count(0) / half
    # Box-drawing chars (U+25xx) put NULs on the "other" side too, so compare ratios.
    if odd > 0.3 and odd > 2 * even:
        return "utf-16-le"
    if even > 0.3 and even > 2 * odd:
        return "utf-16-be"
    return None


def decode_bytes(raw: bytes, forced: str | None = None) -> tuple[str, str, str]:
    """Return (text, encoding, basis). basis tells how sure the choice is."""
    if forced:
        return raw.decode(forced), forced, "forced"
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16"), "utf-16", "bom"
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw[3:].decode("utf-8"), "utf-8-sig", "bom"
    utf16 = _nul_utf16(raw)
    if utf16:
        return raw.decode(utf16, errors="replace"), utf16, "nul-heuristic"
    try:
        text = raw.decode("utf-8")
        return text, "utf-8", "suspect-nul" if "\x00" in text else "strict-decode"
    except UnicodeDecodeError:
        pass
    if any(p in raw for p in _CP850_BOX):
        return raw.decode("cp850"), "cp850", "box-drawing-heuristic"
    try:
        return raw.decode("cp1252"), "cp1252", "fallback-unverified"
    except UnicodeDecodeError:
        return raw.decode("latin-1"), "latin-1", "fallback-unverified"


def connect_rw(db_path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(db_path)
    con.executescript(_SCHEMA)
    return con


def connect_ro(db_path: Path) -> sqlite3.Connection:
    """Search never creates a database: a mistyped path must fail, not abstain."""
    if not db_path.is_file():
        raise FileNotFoundError(f"cache not found: {db_path}")
    return sqlite3.connect(f"file:{db_path.resolve()}?mode=ro", uri=True)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ingest(con: sqlite3.Connection, path: Path, encoding: str | None = None) -> dict[str, object]:
    """Add/replace one tree file; unchanged files (same SHA-256) are skipped."""
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    key = str(path.resolve())
    row = con.execute("SELECT sha256 FROM sources WHERE source_path=?", (key,)).fetchone()
    if row and row[0] == digest:
        return {"source_path": key, "sha256": digest, "action": "unchanged"}
    text, enc, basis = decode_bytes(raw, encoding)
    lines = [ln.rstrip("\r") for ln in text.split("\n")]
    con.execute("DELETE FROM lines WHERE source_path=?", (key,))
    con.executemany(
        "INSERT INTO lines(text, source_path, line_no) VALUES (?,?,?)",
        ((ln.strip(), key, i) for i, ln in enumerate(lines, 1) if ln.strip()),
    )
    con.execute("INSERT OR REPLACE INTO sources VALUES (?,?,?,?,?,?)",
                (key, digest, len(raw), enc, basis, len(lines)))
    con.commit()
    return {"source_path": key, "sha256": digest, "encoding": enc, "encoding_basis": basis,
            "lines": len(lines), "action": "replaced" if row else "added"}


def prune(con: sqlite3.Connection) -> list[dict[str, str]]:
    """Drop cached sources whose file vanished; report changed ones (re-run build)."""
    report: list[dict[str, str]] = []
    for key, digest in con.execute("SELECT source_path, sha256 FROM sources").fetchall():
        p = Path(key)
        if not p.is_file():
            con.execute("DELETE FROM lines WHERE source_path=?", (key,))
            con.execute("DELETE FROM sources WHERE source_path=?", (key,))
            report.append({"source_path": key, "action": "removed-missing"})
        elif _sha256(p) != digest:
            report.append({"source_path": key, "action": "stale-rebuild-needed"})
    con.commit()
    return report


def _fts_query(term: str) -> str:
    """Quote each whitespace token so user input cannot inject FTS5 syntax."""
    return " ".join('"' + t.replace('"', '""') + '"' for t in term.split() if t)


def search(con: sqlite3.Connection, term: str, limit: int = 20,
           verify: bool = False) -> list[dict[str, object]]:
    """Exact-token lookup with provenance; verify=True flags hits from changed/missing files."""
    query = _fts_query(term)
    if not query:
        return []
    limit = max(1, min(int(limit), MAX_LIMIT))
    rows = con.execute(
        "SELECT l.text, l.source_path, l.line_no, s.sha256 FROM lines l "
        "JOIN sources s ON s.source_path = l.source_path "
        "WHERE lines MATCH ? ORDER BY l.source_path, l.line_no LIMIT ?",
        (query, limit),
    ).fetchall()
    current: dict[str, str | None] = {}
    hits: list[dict[str, object]] = []
    for text, path, line_no, digest in rows:
        hit: dict[str, object] = {"text": text, "source_path": path,
                                  "locator": f"line {line_no}", "source_sha256": digest}
        if verify:
            if path not in current:
                current[path] = _sha256(Path(path)) if Path(path).is_file() else None
            hit["stale"] = current[path] != digest
        hits.append(hit)
    return hits


def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("db", type=Path)
    b.add_argument("files", type=Path, nargs="+")
    b.add_argument("--encoding", help="force codec, e.g. cp850, cp1252, utf-16")
    s = sub.add_parser("search", help="exact-token search (no prefix matching)")
    s.add_argument("db", type=Path)
    s.add_argument("term")
    s.add_argument("--limit", type=int, default=20)
    s.add_argument("--verify", action="store_true", help="flag hits from changed files")
    p = sub.add_parser("prune")
    p.add_argument("db", type=Path)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.cmd == "search":
        result: object = search(connect_ro(args.db), args.term, args.limit, args.verify)
    elif args.cmd == "build":
        con = connect_rw(args.db)
        result = [ingest(con, f, args.encoding) for f in args.files]
    else:
        result = prune(connect_rw(args.db))
    json.dump(result, sys.stdout, ensure_ascii=False, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
