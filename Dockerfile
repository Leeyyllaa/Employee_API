# --- Base Image ---
FROM python:3.12-slim


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /app

# Copy only requirements 
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app ./app

# Env vars
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Expose port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
