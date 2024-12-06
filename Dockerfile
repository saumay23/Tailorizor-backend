# Step 1: Use the official Python image
FROM python:3.9-slim

# Step 2: Install system dependencies required by pyppeteer (Chromium)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxi6 libxtst6 libnss3 libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libxrandr2 \
    && rm -rf /var/lib/apt/lists/*

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy the requirements file to the container
COPY requirements.txt .

# Step 5: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the rest of the application code
COPY . .

# Step 7: Expose the port the app will run on
EXPOSE 8000

# Step 8: Set the default command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
