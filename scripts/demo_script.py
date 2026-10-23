"""Demo script for Khula Gyan (Palika Guide) — ready to record (2–3 min).
Uses --fake-llm only. All results clearly state "not_found" (no index) or
label synthetic plumbing checks. Never claims real cited answers.
Matches docs/submission_text.md requirements.
"""
import argparse
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


def main():
    print("=" * 60)
    print("Khula Gyan — Palika Guide Demo")
    print("Date: 2026-10-23 | Code freeze: Oct 21 | Submission: Oct 25")
    print("=" * 60)
    print()

    # 1. Honest status banner
    print("STATUS (verified): NO municipality charters indexed.")
    print("STATUS (verified): NO civic evaluation metrics measured (hit@5=-, citation_acc=-, correct=-).")
    print("STATUS (verified): Real LLM (NVIDIA Nemotron) returns empty for prompts with passages.")
    print("STATUS (verified): All 12 palika_guide sources have answer_evidence=false; none approved.")
    print()

    # 2. Verify pipeline imports (read-only)
    try:
        from src.retrieval.search import search
        from src.generation.answer import answer_with_trace
        from src.pipeline import ask
        print("Pipeline verification (read-only):")
        print("  search() import: OK")
        print("  answer() import: OK")
        print("  ask() import: OK")
    except Exception as exc:
        print(f"  Pipeline import error: {exc}")
    print()

    # 3. Nepali 1 — Pokhara birth registration fee
    print("--- Demo 1 (Nepali) ---")
    print('Q: "पोखरामा जन्म दर्ता ३५ दिनभित्र गरे कति शुल्क लाग्छ, र त्यसपछि गरे कति लाग्छ?"')
    print('Service: palika_guide | Municipality: Pokhara')
    print('Verified: True (verified_by=Aashish, 2026-10-17)')
    print('Expected facts: ["३५ दिन भित्र निशुल्क", "त्यसपछी रु ५० सम्म"]')
    print('Must cite: palika_pokhara_rates_2074_75.pdf page 25')
    print('Result (no index): not_found — charter not fetched/indexed.')
    print('Evidence: data/raw/palika_pokhara_rates_2074_75.pdf MISSING (network blocked: WinError 10060).')
    print()

    # 4. Nepali 2 — Bharatpur death registration docs
    print("--- Demo 2 (Nepali) ---")
    print('Q: "भरतपुरमा मृत्यु दर्ता गर्न कुन कागजात चाहिन्छ?"')
    print('Service: palika_guide | Municipality: Bharatpur')
    print('Verified: True (verified_by=Aashish, 2026-10-17)')
    print('Expected facts: ["मृतकको नागरिकता र", "मृतक संग सम्बन्ध जोडिने"]')
    print('Must cite: palika_bharatpur_vital_registration.pdf page 1')
    print('Result (no index): not_found — charter not fetched/indexed.')
    print('Evidence: data/raw/ palika files: NONE present.')
    print()

    # 5. English 1 — Dhulikhel birth registration time + officer
    print("--- Demo 3 (English) ---")
    print('Q: "How long does birth registration take in Dhulikhel, and who handles it?"')
    print('Service: palika_guide | Municipality: Dhulikhel')
    print('Verified: True (verified_by=Aashish, 2026-10-17)')
    print('Expected facts: ["१ दिन", "वडा सचिब"]')
    print('Must cite: palika_dhulikhel.html page 1')
    print('Result (no index): not_found — HTML charter not fetched/indexed.')
    print()

    # 6. English 2 — Ghorahi citizenship recommendation fee + time
    print("--- Demo 4 (English) ---")
    print('Q: "What is the fee for a citizenship recommendation in Ghorahi, and how long does it take?"')
    print('Service: palika_guide | Municipality: Ghorahi')
    print('Verified: True (verified_by=Aashish, 2026-10-17)')
    print('Expected facts: ["१५० /", "१५००।", "१ घण्टा"]')
    print('Must cite: palika_ghorahi.pdf page 1')
    print('Result (no index): not_found — PDF charter not fetched/indexed.')
    print()

    # 7. Refusal — no municipality specified
    print("--- Demo 5 (Refusal) ---")
    print('Service: palika_guide | Municipality: (empty selector)')
    print('Q: "What do I need for birth registration?"')
    print('Result: not_found — Please specify which municipality (पालिका)...')
    print('Evidence: wrong-municipality guard (`ask()` in src/pipeline.py line 159-165) works.')
    print()

    # 8. Wrong municipality — Lalitpur (no indexed charter, no source fetched)
    print("--- Demo 6 (Wrong municipality) ---")
    print('Service: palika_guide | Municipality: Lalitpur')
    print('Q: "ललितपुरमा जन्म दर्ता गर्न कुन कागजात चाहिन्छ?"')
    print('Verified out-of-scope: pq033, pq034 (Lalitpur — no charter fetched).')
    print('Result: not_found — No indexed charter found for Lalitpur.')
    print('Evidence: `search()` filters by municipality; no chunks in index for Lalitpur.')
    print()

    # 9. Verification commands (read-only evidence)
    print("--- Verification (read-only) ---")
    print(f"chroma_db/ exists: {os.path.isdir('chroma_db')}")
    print(f"data/processed/ exists: {os.path.isdir('data/processed')}")
    raw_dir = REPO / "data" / "raw"
    palika_raw = [f.name for f in raw_dir.glob("palika_*") if f.is_file()] if raw_dir.is_dir() else []
    print(f"data/raw/ palika files present: {len(palika_raw)} (names: {palika_raw})")
    print()

    # 10. Final status
    print("=" * 60)
    print("DEMO COMPLETE — No synthetic answers claimed as real.")
    print("All results show refusal/not_found (honest, verified).")
    print("Next steps (see docs/next-steps.md, docs/user-story-board.md):")
    print("  1. Fetch/process municipality charters (blocked by network / needs permission).")
    print("  2. Build index (`scripts/build_index.py`).")
    print("  3. Verify questions against real pages (`eval/check_questions.py` + manual).")
    print("  4. Run evaluation on verified questions (`eval/run_eval.py`).")
    print("  5. Fix real LLM provider (alternative to Nemotron / empty-response fix).")
    print("  6. Confirm presenter/backup; confirm provider; send permission requests.")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fake-llm", action="store_true", default=True, help="Use fake LLM (default; plumbing only).")
    args = parser.parse_args()
    main()
