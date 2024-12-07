# Use a slim Python base image for efficiency
FROM python:3.9-slim

# Install system dependencies required for Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    ca-certificates \
    fontconfig \
    libx11-xcb1 \
    libxcomposite1 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-6 \
    libgbm1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Download and install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/google-chrome.deb && \
    apt-get update && apt-get install -y /tmp/google-chrome.deb && \
    rm -rf /var/lib/apt/lists/* /tmp/google-chrome.deb

# Set the working directory
WORKDIR /app

# Copy application code into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI app will run on (default: 8000)
EXPOSE 8000

# Run the FastAPI app with Uvicorn, respecting the $PORT environment variable
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
