# Use Python slim base image
FROM python:3.9-slim



# Install system dependencies for Chromium
RUN apt-get update && apt-get install -y \
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
    --no-install-recommends \
    && apt-get clean

RUN apt-get update && apt-get install -y wget

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/google-chrome.deb && \
    apt-get update && apt-get install -y /tmp/google-chrome.deb && \
    rm /tmp/google-chrome.deb

# Set the working directory
WORKDIR /app

# Copy the application code into the container
COPY . .

# Install the required Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port FastAPI app will be running on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
