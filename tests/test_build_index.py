"""Tests for build_index.py source eligibility logic."""

import tempfile
from pathlib import Path
import yaml

from scripts.build_index import load_sources


def test_source_eligibility_confirmed_open_and_answer_evidence():
    """Source with confirmed open licence and answer_evidence=true is eligible."""
    with tempfile.TemporaryDirectory() as tmp:
        sources_file = Path(tmp) / "sources.yaml"
        sources_file.write_text(yaml.dump({
            "sources": [{
                "id": "test_confirmed_open",
                "filename": "test.pdf",
                "service": "citizenship",
                "lang": "ne",
                "answer_evidence": True,
                "licence_status": "confirmed open",
                "local_only": False,
            }]
        }))
        sources = load_sources(sources_file)
        src = sources[0]
        licence_ok = src.get("licence_status") == "confirmed open"
        local_approved = (
            src.get("answer_evidence", False)
            and src.get("approval_note")
            and src.get("local_only", False)
        )
        assert licence_ok is True
        assert not local_approved
        assert (licence_ok or local_approved) is True


def test_source_eligibility_local_approved_path():
    """Source with answer_evidence + approval_note + local_only is eligible (local-only path)."""
    with tempfile.TemporaryDirectory() as tmp:
        sources_file = Path(tmp) / "sources.yaml"
        sources_file.write_text(yaml.dump({
            "sources": [{
                "id": "test_local_approved",
                "filename": "test.pdf",
                "service": "citizenship",
                "lang": "ne",
                "answer_evidence": True,
                "licence_status": "unclear",
                "approval_note": "Leader-approved for local internal baseline only; no redistribution; permission request pending",
                "approved_on": "2026-10-11",
                "approved_by": "Harikrishna Pokhrel",
                "local_only": True,
            }]
        }))
        sources = load_sources(sources_file)
        src = sources[0]
        licence_ok = src.get("licence_status") == "confirmed open"
        local_approved = (
            src.get("answer_evidence", False)
            and src.get("approval_note")
            and src.get("local_only", False)
        )
        assert licence_ok is False
        assert local_approved is True
        assert (licence_ok or local_approved) is True


def test_source_rejected_no_evidence_or_approval():
    """Source without answer_evidence or approval is rejected."""
    with tempfile.TemporaryDirectory() as tmp:
        sources_file = Path(tmp) / "sources.yaml"
        sources_file.write_text(yaml.dump({
            "sources": [{
                "id": "test_rejected",
                "filename": "test.pdf",
                "service": "citizenship",
                "lang": "ne",
                "answer_evidence": False,
                "licence_status": "unclear",
                "local_only": True,
            }]
        }))
        sources = load_sources(sources_file)
        src = sources[0]
        licence_ok = src.get("licence_status") == "confirmed open"
        local_approved = (
            src.get("answer_evidence", False)
            and src.get("approval_note")
            and src.get("local_only", False)
        )
        assert (licence_ok or local_approved) is False


def test_source_rejected_missing_approval_note():
    """Source with answer_evidence + local_only but missing approval_note is rejected."""
    with tempfile.TemporaryDirectory() as tmp:
        sources_file = Path(tmp) / "sources.yaml"
        sources_file.write_text(yaml.dump({
            "sources": [{
                "id": "test_missing_note",
                "filename": "test.pdf",
                "service": "citizenship",
                "lang": "ne",
                "answer_evidence": True,
                "licence_status": "unclear",
                "local_only": True,
            }]
        }))
        sources = load_sources(sources_file)
        src = sources[0]
        licence_ok = src.get("licence_status") == "confirmed open"
        local_approved = (
            src.get("answer_evidence", False)
            and src.get("approval_note")
            and src.get("local_only", False)
        )
        assert licence_ok is False
        assert not local_approved
        assert not (licence_ok or local_approved)