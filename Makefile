run:
	pipenv run python Generate.py

scan:
	pipenv run python Scan.py

train:
	pipenv run python Train.py

format:
	pipenv run isort .
	pipenv run black .