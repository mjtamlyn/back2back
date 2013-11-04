dev:
	PYTHONUNBUFFERED=True foreman start -f DevProcfile

test:
	python manage.py test
