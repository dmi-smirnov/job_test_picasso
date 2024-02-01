FROM python:3.10.12

WORKDIR /usr/src/app

COPY ./django_project .

RUN pip install -r requirements_celery.txt

CMD celery --app django_project worker