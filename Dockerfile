FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements_icelandic.txt .
RUN pip install --no-cache-dir -r requirements_icelandic.txt \
    && pip install cryptography

COPY . .

CMD ["python", "generate_podcast.py"]