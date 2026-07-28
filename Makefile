.PHONY: install lint test validate check

install:
	python -m pip install -r requirements-dev.txt

lint:
	ruff check .

validate:
	python tools/curriculum-validator/validate_metadata.py

test:
	pytest

check: lint validate test
