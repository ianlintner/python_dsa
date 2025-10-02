# Use official Python base image
FROM python:3-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml poetry.lock* requirements.txt* ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install gunicorn

# Copy project
COPY . .

# Build documentation with MkDocs inside a virtual environment
RUN python -m venv /opt/venv \
    && . /opt/venv/bin/activate \
    && pip install --upgrade pip \
    && pip install mkdocs mkdocs-material mkdocs-mermaid2-plugin mkdocs-awesome-pages-plugin mkdocs-git-revision-date-localized-plugin \
    && mkdocs build --clean

# Expose port for Flask app
EXPOSE 5000

# Default command to run Flask app with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "flask_app.app:app"]
