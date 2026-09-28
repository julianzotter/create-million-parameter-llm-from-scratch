"""Record schemas for NEXUS registry, knowledge claims and run reports.

Field sets follow 00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28:
source identity (MUST-30/31, MUST-153), knowledge claim (MUST-66),
run record and result contract (MUST-45, MUST-51, MUST-150/151).
"""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SourceStatus(str, Enum):
    CANONICAL = "CANONICAL"
    REFERENCE = "REFERENCE"
    DERIVED = "DERIVED"
    OBSOLETE = "OBSOLETE"
    UNKNOWN = "UNKNOWN"


class TicketStatus(str, Enum):  # MUST-43/44
    OPEN = "OPEN"
    CLAIMED = "CLAIMED"
    RUNNING = "RUNNING"
    DONE = "DONE"
    BLOCKED = "BLOCKED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    FAILED = "FAILED"


class DevState(str, Enum):  # MUST-55
    REFERENCE = "REFERENCE"
    INTENT_TO_IMPLEMENT = "INTENT_TO_IMPLEMENT"
    EVALUATE = "EVALUATE"
    PROPOSED = "PROPOSED"
    IMPLEMENTED = "IMPLEMENTED"
    TESTED = "TESTED"
    ADOPTED = "ADOPTED"


class SourceIdentity(BaseModel):
    """Identity is established before any semantic enrichment (MUST-32, MUST-153)."""

    source_id: str = Field(description="Drive file ID, git path@sha or other stable ID")
    title: str
    source_uri: str
    representation: str = Field(description="MIME type / export format of the bytes hashed")
    size_bytes: Optional[int] = None
    sha256: Optional[str] = Field(default=None, description="Only set from actual bytes")
    modified_at: Optional[str] = None
    status: SourceStatus = SourceStatus.UNKNOWN
    visibility: str = Field(default="private", description="public|private (MUST-122)")
    # Enrichment never replaces identity (MUST-72).
    labels: list[str] = []
    anchors: list[str] = []
    signals: list[str] = []
    key_values: dict[str, str] = {}


class KnowledgeClaim(BaseModel):
    """Minimum audit fields for retrievable knowledge objects (MUST-66)."""

    claim_id: str
    claim: str
    source_id: str
    source_uri: str
    locator: str = Field(description="page/clause/line/cell; smallest practical (MUST-63)")
    version_or_hash: str
    retrieved_at: str
    authority_level: str
    evidence_type: str
    verification_status: str = "UNVERIFIED"
    agent_id: str
    run_id: str


class Executor(BaseModel):
    """Role, model and runtime are distinct (Manifest §4, MUST-150)."""

    role_id: str
    executor_instance: str
    provider: str
    model_id: str
    runtime: str
    tool_scope: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class RunRecord(BaseModel):
    """Run metadata (MUST-51) + result contract (MUST-45)."""

    run_id: str
    ticket_id: str
    executor: Executor
    started_at: str
    completed_at: Optional[str] = None
    ticket_status: TicketStatus
    dev_state: DevState
    inputs: list[str] = []
    findings: list[str] = []
    evidence: list[str] = []
    artifacts: list[str] = []
    risks: list[str] = []
    next_action: list[str] = Field(default=[], max_length=3)
    qa_status: str = "PENDING"

    def to_markdown(self) -> str:
        """Render the report-back block; empty sections are stated, not dropped (MUST-53)."""
        e = self.executor
        head = [
            f"run_id: {self.run_id}",
            f"ticket_id: {self.ticket_id}",
            f"role_id: {e.role_id} | executor: {e.executor_instance} | "
            f"provider/model: {e.provider}/{e.model_id} | runtime: {e.runtime}",
            f"tool_scope: {e.tool_scope}",
            f"started_at: {self.started_at} | completed_at: {self.completed_at or 'n/a'}",
            f"ticket_status: {self.ticket_status.value} | dev_state: {self.dev_state.value}"
            f" | qa_status: {self.qa_status}",
        ]
        sections = [
            ("INPUTS", self.inputs), ("FINDINGS", self.findings),
            ("EVIDENCE/SOURCES", self.evidence), ("ARTIFACTS", self.artifacts),
            ("RISKS", self.risks), ("NEXT_ACTION", self.next_action),
        ]
        out = ["```", *head, "```"]
        for name, items in sections:
            out.append(f"\n### {name}")
            out.extend(f"- {i}" for i in items) if items else out.append("- (none)")
        return "\n".join(out) + "\n"
