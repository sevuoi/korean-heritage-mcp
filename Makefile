.PHONY: install run run-http test lint format typecheck check

install:
	python3 -m pip install -e ".[dev]"

run:
	python3 -m kakao_heritage

run-http:
	python3 -m kakao_heritage --transport streamable-http

test:
	pytest -q

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy src

check:
	ruff check . && ruff format --check . && mypy src && pytest -q
