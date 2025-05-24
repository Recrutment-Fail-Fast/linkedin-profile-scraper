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
RUN pip install -r requirements.txt

# Set Playwright environment variables before installation
ENV PLAYWRIGHT_BROWSERS_PATH=/root/.cache/ms-playwright
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0

# Install Playwright browsers with explicit path
RUN playwright install --with-deps chromium

# Verify Playwright installation and create compatibility symlink
RUN find /root/.cache/ms-playwright -name "chrome" -type f 2>/dev/null | head -1 > /tmp/chrome_path.txt && \
    if [ -s /tmp/chrome_path.txt ]; then \
    echo "✅ Chrome found at: $(cat /tmp/chrome_path.txt)"; \
    mkdir -p /ms-playwright && \
    ln -sf /root/.cache/ms-playwright/* /ms-playwright/ 2>/dev/null || true; \
    else \
    echo "❌ Chrome not found in expected location"; \
    find / -name "chrome" -type f 2>/dev/null | grep -E "(playwright|chromium)" | head -5; \
    fi

# Copy application code
COPY . .

# Create necessary directories and set proper permissions
RUN mkdir -p /tmp/chrome-profile && \
    chmod 755 /tmp/chrome-profile

# Expose port
EXPOSE 8000

# Set environment variables for containerized Chrome
ENV CHROME_USER_DATA_DIR=/tmp/chrome-profile
ENV CHROME_PROFILE_DIRECTORY=Default
ENV DISPLAY=:99
ENV DOCKER=true

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]