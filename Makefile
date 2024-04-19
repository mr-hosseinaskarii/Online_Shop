.PHONY: exportrequirements
exportrequirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

.PHONY: requirements
requirements:
	poetry init
	poetry add $(cat requirements.txt)

.PHONY: runserver
runserver:
	poetry run python manage.py runserver

.PHONY: createsuperuser
createsuperuser:
	poetry run python manage.py createsuperuser

.PHONY: makemigrations
makemigrations:
	poetry run python manage.py makemigrations

.PHONY: migrate
migrate:
	poetry run python manage.py migrate

.PHONY: test
test:
    poetry run python manage.py test