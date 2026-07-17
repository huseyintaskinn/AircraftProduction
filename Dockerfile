FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /srv/app

# Install system dependencies in a single layer and clean up lists
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    build-essential \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies first (Docker cache optimization)
COPY requirements.txt /srv/app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /srv/app/

# Expose Django port
EXPOSE 8000

# Run collectstatic with dummy environment variables to prevent build failure
RUN DATABASE_URL=sqlite:///:memory: SECRET_KEY=build-time-secret-key-12345 python manage.py collectstatic --noinput