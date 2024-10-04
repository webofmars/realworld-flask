#!/bin/bash

# Wait for the database to be ready
echo "Wait for PostgreSQL to accept connections..."
for i in {1..30}; do
  pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"
  if [ $? -eq 0 ]; then
    echo "DB is ready!"
    break
  fi
  echo "DB not ready to accep connections. Waiting..."
  sleep 1
done

# Run Alembic migrations
alembic upgrade head

# Check the exit status of the Alembic command
if [ $? -eq 0 ]; then
  echo "Alembic migrations succeeded."
else
  echo "Error: Alembic migrations failed."
  exit 1
fi