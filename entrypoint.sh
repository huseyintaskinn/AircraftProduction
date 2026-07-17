#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Creating initial user groups (Wing, Fuselage, Tail, Avionics, Assembly)..."
python manage.py create_groups

# Start server
echo "Starting server..."
exec "$@"
