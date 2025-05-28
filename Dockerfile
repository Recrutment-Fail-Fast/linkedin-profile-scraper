# Use Python 3.11 slim image as base
FROM python:3.11-slim

ARG NODE_MAJOR=20

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
    libatk1.0-0 \
    libdrm2 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxi6 \
    libxtst6 \
    libxss1 \
    libgconf-2-4 \
    libcups2 \
    libdbus-1-3 \
    xdg-utils \
    dbus \
    ca-certificates \
    procps \
    psmisc \
    libgbm1 \
    git \
    fontconfig \
    fonts-dejavu \
    fonts-dejavu-core \
    fonts-dejavu-extra \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js using NodeSource PPA
RUN mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install nodejs -y \
    && rm -rf /var/lib/apt/lists/*

# Verify Node.js and npm installation (optional, but good for debugging)
RUN node -v && npm -v && npx -v

# Create app directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install playwright system dependencies and browsers (required for browser-use)
RUN python -m playwright install-deps chromium
RUN python -m playwright install chromium

# Create directories that browser-use might need
RUN mkdir -p /tmp/chrome-profile /root/.cache

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

ENV DISPLAY=:99
ENV DOCKER=true

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]