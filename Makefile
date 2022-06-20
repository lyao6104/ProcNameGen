run:
	pipenv run python ProcNameGen.py

format:
	pipenv run isort .
	pipenv run black .