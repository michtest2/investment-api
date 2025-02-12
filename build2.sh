#!/usr/bin/env bash
# Exit on error
set -o errexit

# # Install system dependencies
# apt-get update
# apt-get install -y \
#     python3-dev \
#     libpq-dev \
#     gcc \
#     postgresql \
#     postgresql-contrib

# Create virtual environment if it doesn't exist
# python -m venv .venv

# Activate virtual environment
# source .venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install wheel
pip install --no-cache-dir -r requirements.txt

# Only run migrations and collectstatic for web service
# if [ "$RENDER_SERVICE_TYPE" = "web" ]; then
#     python manage.py collectstatic --no-input
#     python manage.py migrate
# fi