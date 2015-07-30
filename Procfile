web: gunicorn otree.wsgi
worker: python manage.py celery worker --app=otree.celery.app:app --loglevel=INFO
