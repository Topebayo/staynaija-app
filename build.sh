#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing requirements..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Generating migrations..."
python manage.py makemigrations

echo "Running migrations..."
python manage.py migrate

echo "Seeding default data (optional)..."
# You can comment this out if you do not want to seed data in production
python manage.py seed_data

echo "Build finished successfully!"
