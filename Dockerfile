FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set workdir inside the container to /app
WORKDIR /app

# Install system dependencies (Authlib and others may need build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI app code
COPY app/ /app

# Copy the keys so ../config/... works from /app
COPY config/ /config

# Expose the port uvicorn will listen on
EXPOSE 8000

# Run the app (same as: cd app && uvicorn main:app ...)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]