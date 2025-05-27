#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

echo "Starting local development environment for AI Ad Generator..."

# Navigate to the frontend directory
echo "Navigating to frontend directory: $(pwd)/frontend"
cd "$(dirname "$0")/../frontend"

# Install frontend dependencies
echo "Installing/updating frontend dependencies..."
npm install

# Build the frontend (output will be copied to backend/app/static by npm script)
echo "Building frontend..."
npm run build

# Navigate to the backend directory
echo "Navigating to backend directory: $(dirname "$0")/../backend"
cd "$(dirname "$0")/../backend"

# Create a Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating Python virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt

# Check if .env file exists, if not, copy from .env.example
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    echo "No .env file found. Copying from .env.example. Please configure it with your GCP details."
    cp .env.example .env
  else
    echo "Warning: No .env or .env.example file found. Backend might not connect to Vertex AI."
  fi
else
  echo ".env file found."
fi

# Start the FastAPI backend server
echo "Starting FastAPI backend server on http://localhost:8000"
echo "The backend will serve the API and the built frontend."
echo "Press Ctrl+C to stop."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Deactivate virtual environment on exit (though script exits before this usually)
deactivate
echo "Local development environment stopped."
