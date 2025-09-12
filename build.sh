#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create static and media directories if they don't exist
mkdir -p static
mkdir -p media

# Apply ALL database migrations (this includes store app migrations)
python manage.py migrate

# Convert static asset files
python manage.py collectstatic --no-input