#!/bin/bash


while ! nc -z db_movie 5432; do
  echo "Waiting for redis..."
  sleep 1
done
echo "Postgres started"


while ! nc -z cache_movie 6379; do
  echo "Waiting for redis..."
  sleep 1
done
echo "Redis started"

while ! nc -z es_movie 9200; do
  echo "Waiting for elasticsearch..."
  sleep 1
done
echo "Elasticsearch started"


while ! nc -z django_movies_admin_panel 8000; do
  echo "Waiting for django movies admin panel..."
  sleep 1
done
echo "Waiting for django movies admin panel started"

python3 main.py