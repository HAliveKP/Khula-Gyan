ifeq ($(OS),Windows_NT)
PYTHON ?= py -3.12
VENV_PY := .venv/Scripts/python.exe
else
PYTHON ?= python3.12
VENV_PY := .venv/bin/python
endif

.PHONY: setup fetch index test eval run

setup:
	$(PYTHON) -m venv .venv && $(VENV_PY) -m pip install --upgrade pip && $(VENV_PY) -m pip install torch==2.14.1 --index-url https://download.pytorch.org/whl/cpu && $(VENV_PY) -m pip install -r requirements.txt --no-cache-dir

fetch:
	$(VENV_PY) scripts/fetch_sources.py

index:
	$(VENV_PY) scripts/build_index.py

test:
	$(VENV_PY) -m pytest -q

eval:
	$(VENV_PY) eval/run_eval.py --note "manual evaluation"

run:
	$(VENV_PY) -m streamlit run frontend/app.py

