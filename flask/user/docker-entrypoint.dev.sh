#!/bin/bash

echo "Waiting for postgres ..."
while ! nc -z db_user $POSTGRES_PORT; do
  sleep 1
done
echo "Postgres started"

echo "Waiting for redis ..."
while ! nc -z cache_user $REDIS_PORT; do
  sleep 1
done

export FLASK_APP=app.py

cd src
#alembic revision --autogenerate -m 'Initial migration.'
#alembic upgrade head

echo "Starting flask app ..."
cd ..
python3 -m flask run --debug --with-threads --host 0.0.0.0 --port 5000
