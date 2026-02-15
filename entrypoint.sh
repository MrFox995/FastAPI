#!/bin/sh
# entrypoint.sh

set -e  # esci se qualcosa fallisce

# Funzione per attendere che Postgres sia pronto
echo "Waiting for Postgres..."
while ! nc -z "$DATABASE_HOSTNAME" "$DATABASE_PORT"; do
  sleep 1
done
echo "Postgres is up!"

# Applica tutte le migrazioni Alembic
echo "Running Alembic migrations..."
alembic upgrade head

# Avvia FastAPI
echo "Starting FastAPI..."
exec uvicorn app.mainORM:app --host 0.0.0.0 --port 8000 --reload
