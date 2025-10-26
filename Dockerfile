# Use official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .
ENV PORT=8080

# Expose port for FastAPI
EXPOSE 8080

# Start the app using uvicorn
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}


