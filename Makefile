all: init lint generate

init:
	python -m pip install -r requirements.txt

lint:
	python -m flake8 *.py

generate:
	python generate.py
