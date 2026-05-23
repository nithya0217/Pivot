# Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to take advantage of Docker's caching engine
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the project files and folders into the container
COPY . .

# Expose port 8000 for FastAPI traffic
EXPOSE 8000

# Start Uvicorn using the platform-assigned PORT environment variable
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --reload"]
