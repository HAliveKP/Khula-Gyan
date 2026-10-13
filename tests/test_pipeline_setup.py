import json
from pathlib import Path
import subprocess
import sys

import chromadb
import fitz

from scripts.process_document import process_document
from src.ingest.chunk import chunk_text
from src.ingest import extract as extract_module
from src.retrieval import search as search_module


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


def test_processor_fixture_chunks_keep_source_and_service(tmp_path):
    source_url = "https://fixture.invalid/page-one.html"
    output = process_document(
        FIXTURES / "page_one.html",
        service="driving_license",
        lang="en",
        source_url=source_url,
        output_directory=tmp_path,
        ocr=False,
    )
    page = json.loads(output.read_text(encoding="utf-8").splitlines()[0])
    chunks = chunk_text(
        page["text"], doc_id=page["id"], source=page["source"], page=page["page"],
        service=page["service"], lang=page["lang"], source_url=page["source_url"],
        chunk_size=300, overlap=0,
    )

    assert chunks
    assert all(chunk["source_url"] == source_url for chunk in chunks)
    assert all(chunk["service"] == "driving_license" for chunk in chunks)


def test_processor_blanks_wrong_script_when_ocr_is_unavailable(tmp_path, monkeypatch):
    source = tmp_path / "synthetic.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Synthetic Latin text standing in for a broken font map. " * 4)
    document.save(source)
    document.close()

    calls = []

    def unavailable_ocr(_page, *, languages):
        calls.append(languages)
        raise RuntimeError("OCR failed: Tesseract binary unavailable in synthetic test.")

    monkeypatch.setattr(extract_module, "_ocr_page", unavailable_ocr)
    output = process_document(
        source,
        service="citizenship",
        lang="ne",
        output_directory=tmp_path / "processed",
    )
    row = json.loads(output.read_text(encoding="utf-8").splitlines()[0])

    assert calls == ["nep+eng"]
    assert row["text"] == ""
    assert row["extraction_status"] == "unusable"
    assert "Tesseract binary unavailable" in row["extraction_note"]


def test_search_limits_scores_and_service_filter(tmp_path, monkeypatch):
    client = chromadb.PersistentClient(path=str(tmp_path / "chroma"))
    collection = client.create_collection("khula_gyan", metadata={"hnsw:space": "cosine"})
    collection.add(
        ids=["fixture_dl", "fixture_citizenship", "fixture_passport"],
        documents=["amber kite north box", "blue drum south shelf", "green cup west desk"],
        metadatas=[
            {"source": "page_one.html", "page": 1, "service": service, "lang": "en",
             "source_url": f"https://fixture.invalid/{service}.html"}
            for service in ("driving_license", "citizenship", "passport")
        ],
        embeddings=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    )

    class FixedQueryEmbedding:
        def encode(self, _texts, **_kwargs):
            class Embedding:
                @staticmethod
                def tolist():
                    return [[1.0, 0.0, 0.0]]

            return Embedding()

    monkeypatch.setattr(search_module, "PERSIST_DIRECTORY", tmp_path / "chroma")
    monkeypatch.setattr(search_module, "_load_model", lambda: FixedQueryEmbedding())
    top = search_module.search("amber kite", k=1)
    filtered = search_module.search("amber kite", k=5, service="citizenship")

    assert len(top) <= 1
    assert all(0.0 <= item["score"] <= 1.0 for item in top + filtered)
    assert filtered
    assert all(item["service"] == "citizenship" for item in filtered)


def test_search_municipality_filter(tmp_path, monkeypatch):
    """Test that search() respects the municipality filter."""
    client = chromadb.PersistentClient(path=str(tmp_path / "chroma"))
    collection = client.create_collection("khula_gyan", metadata={"hnsw:space": "cosine"})
    collection.add(
        ids=["lalitpur_birth", "kathmandu_birth", "pokhara_birth"],
        documents=["Lalitpur birth registration docs", "Kathmandu birth registration docs", "Pokhara birth registration docs"],
        metadatas=[
            {"source": "lalitpur_charter.pdf", "page": 1, "service": "palika_guide", "lang": "ne",
             "municipality": "Lalitpur", "source_url": "https://lalitpur.gov.np/charter.pdf"},
            {"source": "kathmandu_charter.pdf", "page": 1, "service": "palika_guide", "lang": "ne",
             "municipality": "Kathmandu", "source_url": "https://kathmandu.gov.np/charter.pdf"},
            {"source": "pokhara_charter.pdf", "page": 1, "service": "palika_guide", "lang": "ne",
             "municipality": "Pokhara", "source_url": "https://pokhara.gov.np/charter.pdf"},
        ],
        embeddings=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    )

    class FixedQueryEmbedding:
        def encode(self, _texts, **_kwargs):
            class Embedding:
                @staticmethod
                def tolist():
                    return [[1.0, 0.0, 0.0]]

            return Embedding()

    monkeypatch.setattr(search_module, "PERSIST_DIRECTORY", tmp_path / "chroma")
    monkeypatch.setattr(search_module, "_load_model", lambda: FixedQueryEmbedding())

    # Without municipality filter - should return all
    all_results = search_module.search("birth registration", k=5, service="palika_guide")
    assert len(all_results) == 3

    # With municipality filter - should return only Lalitpur
    lalitpur_results = search_module.search("birth registration", k=5, service="palika_guide", municipality="Lalitpur")
    assert len(lalitpur_results) == 1
    assert lalitpur_results[0]["municipality"] == "Lalitpur"
    assert lalitpur_results[0]["source"] == "lalitpur_charter.pdf"

    # With non-existent municipality - should return empty
    empty_results = search_module.search("birth registration", k=5, service="palika_guide", municipality="NonExistent")
    assert empty_results == []


def test_ask_wrong_municipality_guard(tmp_path, monkeypatch):
    """Test wrong-municipality guard in ask(): missing municipality, unknown municipality, valid municipality."""
    import sys
    from importlib import import_module

    # Mock the answer function to return a valid response
    def mock_answer(query, chunks):
        return {
            "status": "answered",
            "language": "en",
            "answer": "Test answer",
            "checklist": {"documents": [], "fees": [], "steps": [], "where": ""},
            "citations": [{"source": "test.pdf", "page": 1, "quote": "test"}],
            "confidence": "high",
            "disclaimer": "Test disclaimer",
        }

    # Set up Chroma with two municipalities
    client = chromadb.PersistentClient(path=str(tmp_path / "chroma"))
    collection = client.create_collection("khula_gyan", metadata={"hnsw:space": "cosine"})
    collection.add(
        ids=["lalitpur_birth", "kathmandu_birth"],
        documents=["Lalitpur birth registration docs", "Kathmandu birth registration docs"],
        metadatas=[
            {"source": "lalitpur_charter.pdf", "page": 1, "service": "palika_guide", "lang": "ne",
             "municipality": "Lalitpur", "source_url": "https://lalitpur.gov.np/charter.pdf"},
            {"source": "kathmandu_charter.pdf", "page": 1, "service": "palika_guide", "lang": "ne",
             "municipality": "Kathmandu", "source_url": "https://kathmandu.gov.np/charter.pdf"},
        ],
        embeddings=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
    )

    class FixedQueryEmbedding:
        def encode(self, _texts, **_kwargs):
            class Embedding:
                @staticmethod
                def tolist():
                    return [[1.0, 0.0, 0.0]]

            return Embedding()

    monkeypatch.setattr(search_module, "PERSIST_DIRECTORY", tmp_path / "chroma")
    monkeypatch.setattr(search_module, "_load_model", lambda: FixedQueryEmbedding())

    # Mock answer module
    import src.generation.answer as answer_module
    monkeypatch.setattr(answer_module, "answer", mock_answer)

    # Import ask after monkeypatching
    pipeline_module = import_module("src.pipeline")

    # Case 1: Missing municipality for palika_guide -> not_found with clarification
    response = pipeline_module.ask("What documents for birth registration?", service="palika_guide", municipality=None)
    assert response["status"] == "not_found"
    assert "municipality" in response["answer"].lower() or "पालिका" in response["answer"]

    # Case 2: Unknown municipality (no indexed charter) -> not_found
    response = pipeline_module.ask("What documents for birth registration?", service="palika_guide", municipality="NonExistent")
    assert response["status"] == "not_found"
    assert "NonExistent" in response["answer"]

    # Case 3: Valid municipality -> answered
    response = pipeline_module.ask("What documents for birth registration?", service="palika_guide", municipality="Lalitpur")
    assert response["status"] == "answered"
    assert response["answer"] == "Test answer"
    runs_dir = tmp_path / "runs"
    result = subprocess.run(
        [
            sys.executable, str(ROOT / "eval" / "run_eval.py"),
            "--questions", str(FIXTURES / "eval_questions.jsonl"),
            "--runs-dir", str(runs_dir), "--mock", "--fake-llm", "--note", "pytest synthetic fixture harness",
        ],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    run_files = list(runs_dir.glob("*.jsonl"))
    assert len(run_files) == 1
    saved = [json.loads(line) for line in run_files[0].read_text(encoding="utf-8").splitlines()]
    assert [record["id"] for record in saved] == ["fixture_verified"]


def test_raw_processed_and_chroma_data_are_not_tracked():
    result = subprocess.run(
        ["git", "-c", f"safe.directory={ROOT.as_posix()}", "ls-files"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    tracked = result.stdout.splitlines()
    forbidden = [
        path for path in tracked
        if path.replace("\\", "/").startswith(("chroma_db/", "data/raw/", "data/processed/"))
    ]
    assert forbidden == []
