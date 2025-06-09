#!/bin/bash
set -e

# Change to the project root directory (parent of the script's directory)
cd "$(dirname "$0")/.."

# --- Check for backend/.env file ---
ENV_FILE="backend/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Environment file '$ENV_FILE' not found."
    echo "Please create it based on 'backend/.env.example' and populate it with your configuration."
    exit 1
fi
echo "Using environment variables from $ENV_FILE"

# Default values - can be overridden by command line arguments
DEFAULT_GCP_PROJECT_ID=$(gcloud config get-value project)
DEFAULT_GCP_REGION="us-central1" # Choose a region that supports your Vertex AI models
DEFAULT_SERVICE_NAME="task3-ai-ad-generator"
DEFAULT_MEMORY="1Gi"
DEFAULT_CPU="1"
DEFAULT_MAX_INSTANCES="2" # Adjust based on expected load

# --- Configuration ---
GCP_PROJECT_ID="${1:-$DEFAULT_GCP_PROJECT_ID}"
GCP_REGION="${2:-$DEFAULT_GCP_REGION}"
SERVICE_NAME="${3:-$DEFAULT_SERVICE_NAME}"
MEMORY="${4:-$DEFAULT_MEMORY}"
CPU="${5:-$DEFAULT_CPU}"
MAX_INSTANCES="${6:-$DEFAULT_MAX_INSTANCES}"

# Derived names
ARTIFACT_REGISTRY_REPO="app-images" # Or your preferred repository name
IMAGE_NAME="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REGISTRY_REPO}/${SERVICE_NAME}"
IMAGE_TAG="latest" # Or use a versioning scheme, e.g., git commit SHA

# --- Helper Functions ---
check_command() {
  if ! command -v "$1" &> /dev/null; then
    echo "Error: $1 is not installed or not in PATH. Please install it."
    exit 1
  fi
}

enable_api() {
  local api_name="$1"
  echo "Checking if $api_name is enabled..."
  if ! gcloud services list --enabled --filter="name:$api_name" --format="value(name)" | grep -q "$api_name"; then
    echo "Enabling $api_name..."
    gcloud services enable "$api_name"
    echo "$api_name enabled."
  else
    echo "$api_name is already enabled."
  fi
}

# --- Pre-flight Checks ---
check_command "gcloud"
# Docker is not required locally as we are using Google Cloud Build.

echo "--- Deployment Configuration ---"
echo "GCP Project ID:       $GCP_PROJECT_ID"
echo "GCP Region:           $GCP_REGION"
echo "Cloud Run Service:    $SERVICE_NAME"
echo "Artifact Registry:    $ARTIFACT_REGISTRY_REPO"
echo "Image Name:           $IMAGE_NAME:$IMAGE_TAG"
echo "Memory:               $MEMORY"
echo "CPU:                  $CPU"
echo "Max Instances:        $MAX_INSTANCES"
echo "------------------------------"

read -p "Proceed with deployment? (y/N): " confirm
if [[ "$confirm" != [yY] ]]; then
  echo "Deployment cancelled."
  exit 0
fi

# --- Enable Necessary APIs ---
enable_api "run.googleapis.com"
enable_api "artifactregistry.googleapis.com"
enable_api "cloudbuild.googleapis.com"
enable_api "logging.googleapis.com"
enable_api "aiplatform.googleapis.com"

# --- Create Artifact Registry Repository (if it doesn't exist) ---
echo "Checking for Artifact Registry repository: $ARTIFACT_REGISTRY_REPO in $GCP_REGION..."
if ! gcloud artifacts repositories describe "$ARTIFACT_REGISTRY_REPO" \
    --project="$GCP_PROJECT_ID" \
    --location="$GCP_REGION" &> /dev/null; then
  echo "Creating Artifact Registry repository: $ARTIFACT_REGISTRY_REPO..."
  gcloud artifacts repositories create "$ARTIFACT_REGISTRY_REPO" \
    --project="$GCP_PROJECT_ID" \
    --repository-format=docker \
    --location="$GCP_REGION" \
    --description="Docker repository for application images"
  echo "Artifact Registry repository created."
else
  echo "Artifact Registry repository already exists."
fi

# --- Build and Push Docker Image using Cloud Build ---
echo "Building and pushing Docker image using Cloud Build..."
echo "Current directory: $(pwd)"
echo "Checking for cloudbuild.yaml:"
ls -l cloudbuild.yaml || echo "cloudbuild.yaml not found by ls!"

# Cloud Build context is the current directory (project root).
# The cloudbuild.yaml file is in the current directory (project root).
gcloud builds submit . \
  --project="$GCP_PROJECT_ID" \
  --config="cloudbuild.yaml" \
  --substitutions="_IMAGE_NAME=${IMAGE_NAME},_IMAGE_TAG=${IMAGE_TAG}" \
  --gcs-log-dir="gs://${GCP_PROJECT_ID}_cloudbuild/logs"

echo "Image built and pushed: ${IMAGE_NAME}:${IMAGE_TAG}"

# --- Deploy to Cloud Run ---
echo "Deploying to Cloud Run service: $SERVICE_NAME in $GCP_REGION..."

# Environment variables will be loaded from the .env file copied into the Docker image.
# No need to set them here via --set-env-vars.

gcloud run deploy "$SERVICE_NAME" \
  --project="$GCP_PROJECT_ID" \
  --image="${IMAGE_NAME}:${IMAGE_TAG}" \
  --platform="managed" \
  --region="$GCP_REGION" \
  --memory="$MEMORY" \
  --cpu="$CPU" \
  --max-instances="$MAX_INSTANCES" \
  --allow-unauthenticated \
  --port=8080 \
  --timeout=300 # Adjust timeout as needed, esp. for AI model calls
  # --service-account=YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com # Recommended for production

SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --project="$GCP_PROJECT_ID" --region="$GCP_REGION" --platform="managed" --format="value(status.url)")

echo "------------------------------"
echo "Deployment successful!"
echo "Service Name: $SERVICE_NAME"
echo "Service URL:  $SERVICE_URL"
echo "------------------------------"

echo "Note: It might take a few moments for the new revision to become fully active."
echo "You may need to grant the Cloud Run service account permissions to access Vertex AI if you haven't already."
echo "The default Compute Engine service account is often used by Cloud Run by default, which might have broad permissions."
echo "For production, create a dedicated service account with minimal necessary roles (e.g., 'Vertex AI User')."
