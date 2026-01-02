FROM python:3.10-slim

# Install system deps
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.7.1
RUN pip install "poetry==$POETRY_VERSION"

# Disable virtualenv creation (important!)
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Copy dependency files first (for Docker cache)
COPY pyproject.toml poetry.lock* ./

# Install deps (including gunicorn)
RUN poetry install --no-interaction --no-ansi --only main

# Copy app code
COPY . .

# Expose port
EXPOSE 5000

# Run with gunicorn
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
CMD ["python", "run.py"]