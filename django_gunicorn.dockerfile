FROM python:3.10.12

WORKDIR /usr/src/app

COPY ./django_project .

RUN pip install -r requirements_django.txt

CMD python manage.py makemigrations api; \
    python manage.py migrate; \
    python manage.py collectstatic --noinput; \
    gunicorn django_project.wsgi -b 0.0.0.0:80