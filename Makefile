.PHONY: help install uninstall run test clean dev

# Default target
help:
	@echo ""
	@echo "Desktop File Maker - Makefile Commands"
	@echo "======================================="
	@echo ""
	@echo "  make install    - Install Desktop File Maker (creates venv, installs deps)"
	@echo "  make uninstall  - Remove Desktop File Maker"
	@echo "  make run        - Run the application"
	@echo "  make test       - Run the test suite"
	@echo "  make clean      - Clean temporary files"
	@echo "  make dev        - Install with development dependencies"
	@echo ""

# Install the application
install:
	@echo "Installing Desktop File Maker..."
	@bash install.sh

# Uninstall the application
uninstall:
	@echo "Uninstalling Desktop File Maker..."
	@rm -rf venv
	@rm -f ~/.local/bin/desktop-file-maker
	@echo "✓ Uninstalled successfully"

# Run the application
run:
	@if [ ! -d venv ]; then \
		echo "Error: Not installed. Run 'make install' first."; \
		exit 1; \
	fi
	@bash -c "source venv/bin/activate && python3 -m src.main"

# Run tests
test:
	@if [ ! -d venv ]; then \
		echo "Error: Not installed. Run 'make install' first."; \
		exit 1; \
	fi
	@bash -c "source venv/bin/activate && python3 -m pytest tests/ -v"

# Run tests with coverage
test-cov:
	@if [ ! -d venv ]; then \
		echo "Error: Not installed. Run 'make install' first."; \
		exit 1; \
	fi
	@bash -c "source venv/bin/activate && python3 -m pytest tests/ -v --cov=src --cov-report=term-missing"

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned"

# Install with dev dependencies
dev:
	@echo "Installing Desktop File Maker with dev dependencies..."
	@if [ ! -d venv ]; then \
		python3 -m venv venv; \
	fi
	@bash -c "source venv/bin/activate && pip install -e '.[dev]'"
	@echo "✓ Installed with dev dependencies"

# Reinstall (clean + install)
reinstall: uninstall install
	@echo "✓ Reinstalled successfully"
