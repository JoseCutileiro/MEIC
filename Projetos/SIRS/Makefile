PYTHON = python3
VENV_DIR = .venv
REQUIREMENTS = requirements.txt

.PHONY: setup install clean activate

setup:
	@$(PYTHON) -m venv $(VENV_DIR)

install:
	@$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)

clean:
	@rm -rf $(VENV_DIR)
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete
