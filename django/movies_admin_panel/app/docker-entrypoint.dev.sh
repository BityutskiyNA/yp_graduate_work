#!/bin/bash

while ! nc -z db_movie $POSTGRES_PORT; do
  echo "Waiting for postgres..."
  sleep 1
done
echo "PostgreSQL started"

python3 manage.py migrate admin 
python3 manage.py migrate auth 
python3 manage.py migrate contenttypes 
python3 manage.py migrate sessions

# # раскомментировать, если удалены скрипты миграций
# python3 manage.py makemigrations src --settings=config.settings 

python3 manage.py migrate --fake src

python3 manage.py createsuperuser --noinput
python3 manage.py collectstatic --noinput

python3 manage.py runserver 0.0.0.0:8000

exec "$@"



