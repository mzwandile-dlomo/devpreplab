FROM python:3.11-slim

# Create a non-root user for safety
RUN useradd -m runner

WORKDIR /workspace

# Install any minimal tools you might need (e.g., timeout)
RUN apt-get update \
    && apt-get install -y --no-install-recommends time \
    && rm -rf /var/lib/apt/lists/*

USER runner

# By default, just sleep – actual commands are provided by the backend via Docker SDK
CMD ["sleep", "infinity"]