.PHONY: install test run

install:
	python -m pip install -r requirements.txt

test:
	python -m unittest discover -s tests -v

run:
	uvicorn app.main:app --reload
