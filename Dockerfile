FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libfreetype6-dev \
    libpng-dev && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MATPLOTLIBRC=/config/matplotlib \
    PYTHONPATH=/app/src

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

# Copy entire src directory
COPY src/ src/

# Create input/output directories
RUN mkdir -p /mnt/data /mnt/output /mnt/resources

# Copy resource
COPY resources/ /mnt/resources/

# Copy input files into /mnt/input
COPY input/ /mnt/data/


COPY script.sh .
# Give execute permission to the script
RUN chmod +x script.sh

# Run the shell script when the container starts
CMD ["./script.sh"]