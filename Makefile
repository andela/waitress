NAME=waitress

lint:
	black . && isort -rc .

test:
	coverage run waitress/manage.py test

run-backup:
	pipenv run python backup/main.py
