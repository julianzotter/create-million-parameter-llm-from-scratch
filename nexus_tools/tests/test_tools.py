from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from nexus_tools import dup_scan, tree_query
from nexus_tools.schema import DevState, Executor, RunRecord, TicketStatus

TREE = "G:.\n├───_INDEX\n│   └───SEILSTATIK-BOEBLINGEN\n└───LLM-LOCAL-SSOT\n    └───WORK\n"


@pytest.fixture()
def con(tmp_path: Path):
    return tree_query.connect(tmp_path / "cache.db")


def test_decode_utf16_bom() -> None:
    text, enc = tree_query.decode_bytes(TREE.encode("utf-16"))
    assert enc == "utf-16" and "SEILSTATIK" in text


def test_decode_cp850_fallback() -> None:
    raw = "Ablage\\Übersicht".encode("cp850")
    text, enc = tree_query.decode_bytes(raw)
    assert enc == "cp850" and text.endswith("Übersicht")


def test_search_returns_locator_and_hash(con, tmp_path: Path) -> None:
    f = tmp_path / "TREE_A.txt"
    f.write_text(TREE, encoding="utf-8")
    info = tree_query.ingest(con, f)
    hits = tree_query.search(con, "SEILSTATIK")
    assert len(hits) == 1
    assert hits[0]["locator"] == "line 3"
    assert hits[0]["source_sha256"] == info["sha256"]


def test_unchanged_file_is_skipped(con, tmp_path: Path) -> None:
    f = tmp_path / "TREE_A.txt"
    f.write_text(TREE, encoding="utf-8")
    assert tree_query.ingest(con, f)["action"] == "added"
    assert tree_query.ingest(con, f)["action"] == "unchanged"
    f.write_text(TREE + "NEU\n", encoding="utf-8")
    assert tree_query.ingest(con, f)["action"] == "replaced"
    assert len(tree_query.search(con, "WORK")) == 1  # no duplicate rows after replace


def test_search_abstains_and_resists_fts_syntax(con, tmp_path: Path) -> None:
    f = tmp_path / "TREE_A.txt"
    f.write_text(TREE, encoding="utf-8")
    tree_query.ingest(con, f)
    assert tree_query.search(con, "NICHTVORHANDEN") == []
    assert tree_query.search(con, 'WORK" OR "x') == []  # quoted, no injection
    assert tree_query.search(con, "   ") == []


def _f(i: str, title: str, size: int | None, **kw) -> dict:
    return {"id": i, "title": title, "size": size, **kw}


def test_dup_scan_classifications() -> None:
    files = [
        _f("a", "X.txt", 100), _f("b", "X.txt", 100),                       # title+size
        _f("c", "K.txt", 5000, md5="h1"), _f("d", "N.txt", 5000, md5="h1"),  # hash
        _f("e", "S.md", 3000), _f("f", "S.md", None, mimeType=dup_scan.SHORTCUT_MIME),
        _f("g", "R_v1.0.md", 2000), _f("h", "R_v1.1.md", 2000),           # version pair
    ]
    kinds = {f["classification"]: {x["id"] for x in f["files"]} for f in dup_scan.scan(files)}
    assert kinds["DUPLICATE_CANDIDATE"] == {"a", "b"}
    assert kinds["CONTENT_HASH_MATCH"] == {"c", "d"}
    assert "SIZE_ONLY_HINT" not in kinds  # version pair not flagged
    assert all("e" not in ids and "f" not in ids for ids in kinds.values())


def test_run_record_markdown_and_next_action_limit() -> None:
    ex = Executor(role_id="ID06", executor_instance="cc-session", provider="Anthropic",
                  model_id="m", runtime="Claude Code cloud", tool_scope="repo+drive")
    rec = RunRecord(run_id="R1", ticket_id="T1", executor=ex, started_at="t0",
                    ticket_status=TicketStatus.REVIEW_REQUIRED,
                    dev_state=DevState.TESTED, findings=["f1"])
    md = rec.to_markdown()
    assert "role_id: ID06" in md and "### RISKS\n- (none)" in md
    with pytest.raises(ValidationError):
        RunRecord(run_id="R", ticket_id="T", executor=ex, started_at="t",
                  ticket_status=TicketStatus.OPEN, dev_state=DevState.PROPOSED,
                  next_action=["1", "2", "3", "4"])
