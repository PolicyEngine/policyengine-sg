all: install format test

documentation:
	myst build docs -o docs/_build

format:
	black . -l 79
	linecheck . --fix

check-vectorization:
	uv run python check_vectorization.py policyengine_sg/variables

install:
	uv pip install --system -e .[dev]

test:
	uv run pytest policyengine_sg/tests -v

test-cov:
	uv run pytest policyengine_sg/tests --cov=policyengine_sg --cov-report=term-missing

test-lite:
	uv run pytest policyengine_sg/tests/policy -v

build:
	python -m build

changelog:
	python .github/bump_version.py
	towncrier build --yes --version $$(python -c "import re; print(re.search(r'version = \"(.+?)\"', open('pyproject.toml').read()).group(1))")

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build dist *.egg-info .coverage htmlcov

.PHONY: all documentation format install test test-cov test-lite build changelog clean check-vectorization