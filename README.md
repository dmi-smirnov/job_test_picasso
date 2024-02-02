# Документация

## Подготовка файла с переменными окружения
В директории проекта создать файл `.env` со следующими переменными окружения:
```
PROJECT_NAME='django_project'

CELERY_APP_NAME=${PROJECT_NAME}

DJANGO_SECRET_KEY='...'
DJANGO_DEBUG=
DJANGO_ALLOWED_HOSTS='...'

DB_ENGINE='django.db.backends.postgresql'
DB_PORT='5432'
DB_USER=${PROJECT_NAME}
DB_PWD='...'
DB_NAME=${PROJECT_NAME}

HTTP_SRV_ADDR_PORT='127.0.0.1:80'
WEB_SRV_ADDR='...'
```
`DJANGO_SECRET_KEY='...'` вместо `...` подставить SECRET KEY для Django

`DJANGO_DEBUG=` режим DEBUG для Django (любое значение для включения)

`DJANGO_ALLOWED_HOSTS='...'` вместо `...` подставить адреса разрешённых хостов для Django, разделённые пробелом или `*` для разрешения всех хостов

`DB_PWD='...'` вместо `...` подставить пароль, который будет использоваться для БД

`HTTP_SRV_ADDR_PORT='127.0.0.1:80'` адрес и порт, по которым будет доступно приложение на хосте

`WEB_SRV_ADDR='...'` адрес (опционально и порт), по которым будет доступно приложение из сети

## Запуск контейнеров для приложения
Из директории проекта выполнить:
```bash
sudo docker compose up -d
```

## Тестирование приложения
- После запуска контейнеров выполнить из директории проекта:
```bash
sudo docker compose ps
```
- Скопировать имя контейнера для сервиса `django_gunicorn`
- Подключиться к контейнеру, выполнив из директории проекта:
```bash
sudo docker exec -it container_name bash
```
- В контейнере выполнить:
```bash
pip install -r requirements_tests.txt
pytest
```

