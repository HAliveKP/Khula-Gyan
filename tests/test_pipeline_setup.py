import json
from pathlib import Path
import subprocess
import sys

import chromadb

from scripts.process_document import process_document
from src.ingest.chunk import chunk_text
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


def test_eval_runner_writes_results_and_skips_drafts(tmp_path):
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
        and Path(path).name != ".gitkeep"
    ]
    assert forbidden == []

