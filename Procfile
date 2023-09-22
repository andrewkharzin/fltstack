web: gunicorn core.wsgi:application

release: django-admin migrate --no-input && python3 manage.py collectstatic --no-input

