.PHONY: validate build test

validate:
	python scripts/validate_data.py

build:
	python scripts/build_outputs.py

test:
	PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'
