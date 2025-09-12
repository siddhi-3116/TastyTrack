#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create static and media directories if they don't exist
mkdir -p static
mkdir -p media

# Apply ALL database migrations (including your store app)
python manage.py migrate
python manage.py migrate store  # Specifically migrate your store app

# Convert static asset files
python manage.py collectstatic --no-input