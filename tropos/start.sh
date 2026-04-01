#!/bin/bash

# ------------------------------
# Script to start Redis and Django
# ------------------------------

# Step 0: Activate virtual environment if not already active
if [ -z "$VIRTUAL_ENV" ]; then
  echo "Activating virtual environment..."
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source .venv/Scripts/activate
  else
    # Linux / macOS
    source .venv/bin/activate
  fi
else
  echo "Virtual environment already active."
fi

# Step 0.5: Ensure Redis stops when script exits
trap "echo 'Stopping Redis...'; docker-compose down" EXIT

# Step 1: Start Redis container
echo "Starting Redis..."
docker-compose up -d

# Step 2: Wait until Redis is ready
echo "Waiting for Redis to be ready..."
until docker exec $(docker ps -qf "name=redis") redis-cli ping | grep -q PONG; do
  echo -n "."
  sleep 1
done

echo "Redis is ready!"

# Step 3: Start Django development server
echo "Starting Django server..."
python manage.py runserver
