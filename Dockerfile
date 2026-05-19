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

# Start Uvicorn with auto-reload enabled for live development
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
