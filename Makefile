.PHONY: help install lint format check test clean

# Default target
help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  lint       - Run all linting tools"
	@echo "  format     - Format code with black and isort"


	@echo "  test       - Run tests (placeholder)"
	@echo "  clean      - Clean up cache files"
	@echo "  pre-commit - Install pre-commit hooks"

# Install dependencies
install:
	pip install -r requirements.txt

# Install pre-commit hooks
pre-commit:
	pre-commit install

# Format code
format:
	black .
	isort .

# Run all linting tools
lint: format
	flake8 .
	pylint app/ --disable=C0114,C0115,C0116,R0903,R0913,R0914,R0915,C0103,W0621,W0611,W0612,W0613,W0703,W0702,W0511,W0603,W0602,W0601,W0622





# Run tests (placeholder for future test setup)
test:
	python -m pytest tests/

# Clean up cache files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +



# Quick check - run format and basic linting
quick: format
	flake8 .

# Full check - run everything
full: lint
	@echo "Full code quality check completed!"

# Development setup
dev-setup: install pre-commit
	@echo "Development environment setup complete!"
	@echo "Run 'make format' to format code"
	@echo "Run 'make lint' to check code quality"
	@echo "Run 'make full' for comprehensive checks"

# Run tests
pytest:
	pytest tests/

# Run tests with coverage
coverage:
	pytest --cov=app --cov-report=term-missing tests/
