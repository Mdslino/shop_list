SHELL := /bin/bash
CURRENT_DIR := $(shell pwd)
.PHONY: test clean

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build

test:
	@PYTHONPATH=$(CURRENT_DIR) pytest -x -v --cov=./shop_list --cov-report term-missing tests/

requirements:
	@echo "Iniciando a criação de $(CURRENT_DIR)/requirements.txt"
	@poetry export --with-credentials --without-hashes -f requirements.txt --output requirements.txt
	@cat requirements.txt | awk '{print $$1}' | sed 's/;//' | tee requirements.txt
	@echo "Finalizado a criação de $(CURRENT_DIR)/requirements.txt"