#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for PostgreSQL..."
until pg_isready -h db -p 5432 -U ${POSTGRES_USER:-shiprocket_user}; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL started"

# Run migrations
echo "Running database migrations..."
mkdir -p alembic/versions
alembic upgrade head

# Start application
echo "Starting application..."
exec "$@"
