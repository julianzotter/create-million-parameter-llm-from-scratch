from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from nexus_tools import dup_scan, tree_query
from nexus_tools.schema import DevState, Executor, RunRecord, SourceIdentity, TicketStatus

TREE = "G:.\n├───_INDEX\n│   └───SEILSTATIK-BOEBLINGEN\n└───LLM-LOCAL-SSOT\n    └───WORK\n"


@pytest.fixture()
def con(tmp_path: Path) -> Iterator[sqlite3.Connection]:
    c = tree_query.connect_rw(tmp_path / "cache.db")
    yield c
    c.close()


def _tree(tmp_path: Path, text: str = TREE, name: str = "TREE_A.txt") -> Path:
    f = tmp_path / name
    f.write_text(text, encoding="utf-8")
    return f


# --- decoding -------------------------------------------------------------

@pytest.mark.parametrize("codec,expected", [("utf-16", "utf-16"), ("utf-16-le", "utf-16-le"),
                                            ("utf-16-be", "utf-16-be")])
def test_decode_utf16_with_and_without_bom(codec: str, expected: str) -> None:
    text, enc, _ = tree_query.decode_bytes(TREE.encode(codec))
    assert enc == expected and "SEILSTATIK" in text and "\x00" not in text


def test_decode_cp850_tree_vs_cp1252_text() -> None:
    text, enc, basis = tree_query.decode_bytes("├───Übersicht".encode("cp850"))
    assert (enc, basis) == ("cp850", "box-drawing-heuristic") and text == "├───Übersicht"
    text, enc, _ = tree_query.decode_bytes("Übersicht – €".encode("cp1252"))
    assert enc == "cp1252" and text == "Übersicht – €"


def test_decode_forced_encoding() -> None:
    assert tree_query.decode_bytes("Ä".encode("cp1252"), "cp1252")[1:] == ("cp1252", "forced")


# --- cache / search ---------------------------------------------------------

def test_search_returns_locator_and_hash(con: sqlite3.Connection, tmp_path: Path) -> None:
    info = tree_query.ingest(con, _tree(tmp_path))
    hits = tree_query.search(con, "SEILSTATIK")
    assert len(hits) == 1 and hits[0]["locator"] == "line 3"
    assert hits[0]["source_sha256"] == info["sha256"]


def test_delta_and_path_normalisation(con: sqlite3.Connection, tmp_path: Path,
                                      monkeypatch: pytest.MonkeyPatch) -> None:
    f = _tree(tmp_path)
    assert tree_query.ingest(con, f)["action"] == "added"
    monkeypatch.chdir(tmp_path)
    assert tree_query.ingest(con, Path("TREE_A.txt"))["action"] == "unchanged"  # relative path
    f.write_text(TREE + "NEU\n", encoding="utf-8")
    assert tree_query.ingest(con, f)["action"] == "replaced"
    assert len(tree_query.search(con, "WORK")) == 1


def test_prune_and_verify_detect_stale(con: sqlite3.Connection, tmp_path: Path) -> None:
    a, b = _tree(tmp_path), _tree(tmp_path, name="TREE_B.txt")
    tree_query.ingest(con, a)
    tree_query.ingest(con, b)
    b.write_text(TREE + "X\n", encoding="utf-8")
    assert {h["stale"] for h in tree_query.search(con, "WORK", verify=True)} == {False, True}
    a.unlink()
    actions = {r["action"] for r in tree_query.prune(con)}
    assert actions == {"removed-missing", "stale-rebuild-needed"}
    assert len(tree_query.search(con, "WORK")) == 1


def test_search_abstains_and_resists_fts_syntax(con: sqlite3.Connection, tmp_path: Path) -> None:
    tree_query.ingest(con, _tree(tmp_path))
    assert tree_query.search(con, "NICHTVORHANDEN") == []
    assert tree_query.search(con, 'WORK" OR "x') == []
    assert tree_query.search(con, "   ") == []
    assert len(tree_query.search(con, "WORK", limit=-1)) == 1  # clamped to >= 1


def test_connect_ro_never_creates_db(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        tree_query.connect_ro(tmp_path / "typo.db")
    assert not (tmp_path / "typo.db").exists()


def test_line_numbers_ignore_form_feed(con: sqlite3.Connection, tmp_path: Path) -> None:
    tree_query.ingest(con, _tree(tmp_path, "a\fb\nZIEL\n"))
    assert tree_query.search(con, "ZIEL")[0]["locator"] == "line 2"


# --- duplicate scan ---------------------------------------------------------

def _f(i: str | None, title: str | None, size: Any, **kw: Any) -> dict[str, Any]:
    return {"id": i, "title": title, "size": size, **kw}


def _pairs(result: dict[str, Any]) -> dict[frozenset[str], str]:
    return {frozenset(x["id"] for x in f["files"]): f["basis"] for f in result["findings"]}


def test_dup_scan_bases_and_string_sizes() -> None:
    res = dup_scan.scan([
        _f("a", "X.txt", "100"), _f("b", "X.txt", 100),               # str vs int size
        _f("c", "K.txt", 5000, md5="h1"), _f("d", "N.txt", 5000, md5="h1"),
        _f("e", "S.md", "1,5 KB"), _f("f", "S.md", 3000, mimeType=dup_scan.SHORTCUT_MIME),
        _f(None, "ohne-id", 1), _f("g", "Doc", None, mimeType="application/vnd.google-apps.document"),
    ])
    pairs = _pairs(res)
    assert pairs == {frozenset("ab"): "title_size", frozenset("cd"): "content_hash"}
    assert all(f["classification"] == "DUPLICATE_CANDIDATE" for f in res["findings"])
    assert len(res["skipped"]) == 1 and res["not_comparable"] == 2  # "1,5 KB" + native doc


def test_dup_scan_version_and_in_out_pairs_excluded_per_pair() -> None:
    res = dup_scan.scan([
        _f("v1", "R_v1.0.md", 2000), _f("v2", "R v1.1.md", 2000),    # version pair
        _f("i", "A_IN.md", 3000), _f("o", "A_OUT.md", 3000),          # IN/OUT pair
        _f("p", "P.md", 4000), _f("q", "Q.md", 4000), _f("r", "R_v1.0.md", 4000),
    ])
    pairs = _pairs(res)
    assert frozenset({"v1", "v2"}) not in pairs and frozenset("io") not in pairs
    assert {frozenset("pq"), frozenset("pr"), frozenset("qr")} <= set(pairs)  # not suppressed


def test_dup_scan_reports_each_pair_once_under_strongest_basis() -> None:
    res = dup_scan.scan([_f("a", "A.txt", 9000, md5="h"), _f("b", "B.txt", 9000, md5="h"),
                         _f("c", "C.txt", 9000)])
    pairs = _pairs(res)
    assert pairs[frozenset("ab")] == "content_hash"
    assert len(res["findings"]) == 3


# --- schema -----------------------------------------------------------------

def _executor() -> Executor:
    return Executor(role_id="ID06", executor_instance="cc-session", provider="Anthropic",
                    model_id="m", runtime="Claude Code cloud", tool_scope="repo+drive")


def test_run_record_markdown_and_limits() -> None:
    rec = RunRecord(run_id="R1", ticket_id="T1", executor=_executor(), started_at="t0",
                    ticket_status=TicketStatus.REVIEW_REQUIRED, dev_state=DevState.TESTED,
                    findings=["zeile1\nzeile2"], evidence_hashes={"scan": "ab" * 32})
    md = rec.to_markdown()
    assert "role_id: ID06" in md and "### RISKS\n- (none)" in md
    assert "- zeile1 zeile2" in md and "evidence_status: UNVERIFIED" in md
    with pytest.raises(ValidationError):
        RunRecord(run_id="R", ticket_id="T", executor=_executor(), started_at="t",
                  ticket_status=TicketStatus.OPEN, dev_state=DevState.PROPOSED,
                  next_action=["1", "2", "3", "4"])


def test_source_identity_rejects_bad_hash() -> None:
    with pytest.raises(ValidationError):
        SourceIdentity(source_id="x", title="t", source_uri="u", representation="text/plain",
                       sha256="not-a-hash")


def test_dup_scan_ignores_same_id_listed_twice() -> None:
    """Paginated Drive listings can repeat an entry; same ID is not a duplicate."""
    res = dup_scan.scan([_f("x", "verwaltung.csv", 741), _f("x", "verwaltung.csv", 741)])
    assert res["findings"] == []
