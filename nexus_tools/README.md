# nexus_tools — NEXUS ID06 deterministic helpers

Status: **TESTED** (MUST-55), not ADOPTED. Canonical repository for NEXUS code
is still an open ID01 decision (proposal E1); this location is provisional.

Governance: `00_NEXUS_MANIFEST__CURRENT__2026-09-28`,
`00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28` (Drive, `_developement/LLM-LOCAL-SSOT/`).

| Module | Purpose | Writes |
|---|---|---|
| `schema.py` | pydantic models: `SourceIdentity`, `KnowledgeClaim`, `Executor`, `RunRecord` | none |
| `tree_query.py` | FTS5 query cache over existing TREE/DIRLIST text exports; hits carry source path, SHA-256, line locator | local cache DB only (DERIVED) |
| `dup_scan.py` | duplicate *candidates* from a file-metadata JSON listing (MUST-157) | none (stdout) |

## Usage

```bash
pip install pydantic pytest
python -m pytest -q nexus_tools

# tree lists (run where the TREE files live, e.g. G:\Meine Ablage\_INDEX.MASTER)
python -m nexus_tools.tree_query build tree_cache.db TREE-LIST_C_KI-Wissensbasis.txt TREE-LIST_LAUFWERK_D.txt
python -m nexus_tools.tree_query search tree_cache.db "SEILSTATIK" --limit 20

# duplicate candidates from a listing [{"id","title","size","mimeType","parent","md5"?}]
python -m nexus_tools.dup_scan listing.json > dup_candidates.json
```

`tree_cache.db` is a derived, rebuildable cache — not a new canonical index
(MUST-24). Re-running `build` skips files whose SHA-256 is unchanged.
