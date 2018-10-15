all: init lint test generate

init:
	python -m pip install -r requirements.txt

lint:
	python -m pip check
	python -m flake8 *.py

test:
	python -m pytest -v

generate:
	python generate.py
