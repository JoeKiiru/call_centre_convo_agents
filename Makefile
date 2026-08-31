SYSTEM_PYTHON?=python3
VENV?=venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: help init venv install run test clean

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  init    Create virtualenv and install requirements"
	@echo "  venv    Create virtualenv"
	@echo "  install Install requirements into virtualenv"
	@echo "  run     Run the FastAPI app with uvicorn (no activate required)"
	@echo "  test    Run pytest using the virtualenv python"
	@echo "  clean   Remove virtualenv and python caches"

venv:
	$(SYSTEM_PYTHON) -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

init: install

run:
	$(PYTHON) -m uvicorn src.main:app --reload

test:
	$(PYTHON) -m pytest

clean:
	rm -rf $(VENV) .pytest_cache build dist *.egg-info __pycache__
