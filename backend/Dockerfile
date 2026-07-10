FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project (respects .dockerignore)
COPY . .

# Expose port (default 8000, overridden by $PORT on Railway)
EXPOSE 8000

# Use shell form so $PORT is expanded at runtime
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
