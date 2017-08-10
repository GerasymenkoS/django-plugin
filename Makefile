HOST=127.0.0.1

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

test: clean-pyc
	python manage.py test Templarbit

run:
	python manage.py runserver
