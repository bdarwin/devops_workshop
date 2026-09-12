install:  ; python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
run:      ; .venv/bin/uvicorn app.main:app --reload
test:     ; .venv/bin/pytest -q
lint:     ; .venv/bin/ruff check app tests evals
eval:     ; .venv/bin/python evals/run_eval.py
docker:   ; docker build -t concierge:local .
.PHONY: install run test lint eval docker
