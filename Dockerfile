# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy src directory contents into the container
COPY src/ ./src

# Copy main.py into the container
COPY main.py .

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

# Run the scraper when the container launches
CMD ["python", "main.py"]