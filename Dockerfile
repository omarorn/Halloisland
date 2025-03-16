FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
COPY requirements_icelandic.txt .

# Copy application code first
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements_icelandic.txt
RUN pip install -e .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "api.py"]