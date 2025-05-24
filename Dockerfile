# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install browser-use (since it's not in requirements.txt)
RUN pip install browser-use

# Install Playwright and browsers
RUN pip install playwright
RUN playwright install chromium
RUN playwright install-deps

# Copy application code
COPY . .

# Create necessary directories and set proper permissions
RUN mkdir -p /tmp/chrome-profile && \
    chmod 755 /tmp/chrome-profile

# Expose port
EXPOSE 8000

# Set environment variables for containerized Chrome
# Get the actual Playwright Chromium path
RUN PLAYWRIGHT_CHROMIUM_PATH=$(find /ms-playwright -name chrome -type f | head -1) && \
    echo "CHROME_PATH=${PLAYWRIGHT_CHROMIUM_PATH}" >> /etc/environment

ENV CHROME_USER_DATA_DIR=/tmp/chrome-profile
ENV CHROME_PROFILE_DIRECTORY=Default
ENV DISPLAY=:99
ENV DOCKER=true

# Start Xvfb and run the application
CMD Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 & \
    export CHROME_PATH=$(find /ms-playwright -name chrome -type f | head -1) && \
    exec uvicorn main:app --host 0.0.0.0 --port 8000 