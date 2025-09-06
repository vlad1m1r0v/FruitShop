#!/bin/bash
echo "Collecting static files..."
make collect_static

echo "Waiting for postgres..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

echo "Applying migrations..."
make migrate

echo "Filling DB with data..."
make init

exec "$@"