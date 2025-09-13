#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# ✅ ADD THIS SUPERUSER CREATION CODE AT THE END:
echo "=== Creating Superuser ==="
python -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
if username and email and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print('✅ SUPERUSER CREATED SUCCESSFULLY!')
        print('Username:', username)
        print('Email:', email)
    else:
        print('ℹ️ Superuser already exists.')
else:
    print('❌ Superuser environment variables not set.')
    print('Username available:', username is not None)
    print('Email available:', email is not None)
    print('Password available:', password is not None)
"
echo "=== Superuser creation completed ==="