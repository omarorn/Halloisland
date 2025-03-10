# Build stage with CUDA
FROM nvidia/cuda:12.1.1-base-ubuntu22.04 as builder

WORKDIR /app
COPY requirements_icelandic.txt .
RUN apt-get update && apt-get install -y python3.10 python3-pip
RUN pip install --user --no-cache-dir -r requirements_icelandic.txt

# Runtime stage with CUDA
FROM nvidia/cuda:12.1.1-base-ubuntu22.04
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV NVIDIA_VISIBLE_DEVICES=all

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /root/.local /root/.local
COPY . .

# Ensure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Runtime dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Run as non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["python", "generate_podcast.py"]