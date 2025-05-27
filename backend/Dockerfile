# Stage 1: Build React frontend
FROM node:18-alpine as frontend-builder
WORKDIR /app/frontend

# Copy package.json and package-lock.json (or yarn.lock)
COPY frontend/package*.json ./

# Install frontend dependencies
# Using ci for cleaner installs if package-lock.json is robust
RUN npm ci

# Copy the rest of the frontend source code
COPY frontend/ ./

# Build the frontend application
# The output should go to a 'build' or 'dist' folder (e.g., /app/frontend/build)
# Ensure your React app's build script (in package.json) outputs to a known directory.
# If using Vite, it might be 'dist'. For CRA, it's 'build'.
RUN npm run build:docker

# Stage 2: Python backend
FROM python:3.10-slim
WORKDIR /app

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies if any (e.g., for certain Python packages)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code
# This assumes your FastAPI app is in 'backend/app'
COPY backend/app/ ./app/

# Copy built frontend assets from the builder stage into the backend's static serving directory
# Adjust the source path (/app/frontend/build or /app/frontend/dist) based on your React build output directory.
COPY --from=frontend-builder /app/frontend/build ./app/static

# Expose the port the app runs on
EXPOSE 8080

# Command to run the Uvicorn server
# The app.main:app refers to the 'app' instance in 'app/main.py'
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
