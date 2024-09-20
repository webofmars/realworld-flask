#!/bin/bash

# Run Alembic migrations
alembic upgrade head

# Check the exit status of the Alembic command
if [ $? -eq 0 ]; then
  echo "Alembic migrations succeeded."
else
  echo "Error: Alembic migrations failed."
  exit 1
fi