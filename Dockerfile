FROM python:3.11.5-slim-bullseye

WORKDIR /app

# Install system dependencies with retry mechanism
RUN for i in $(seq 1 3); do \
        (apt-get update -y && \
         apt-get install -y --no-install-recommends \
            build-essential \
            curl \
            software-properties-common && \
         apt-get clean && \
         rm -rf /var/lib/apt/lists/*) && break || \
        if [ $i -eq 3 ]; then exit 1; fi; \
        sleep 1; \
    done

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
COPY requirements_icelandic.txt .

# Copy application code first
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements_icelandic.txt
RUN pip install -e .

# Expose port 80 for Railway deployment
EXPOSE 80

# Command to run the application
CMD ["python", "api.py"]