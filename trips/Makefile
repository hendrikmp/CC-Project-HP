# Makefile
.PHONY: test lint

test:
	PYTHONPATH=$(PWD) pytest -v --maxfail=1 
# --disable-warnings

lint:
	flake8 src tests