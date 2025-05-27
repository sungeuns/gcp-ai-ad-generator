# Project Alchemy Task 3 - AI Ad Generator

This project is a web application that generates targeted advertisement copy and images based on customer sentiment (positive or negative).

Note that almost all code was generated using `gemini-2.5-pro-preview-05-06`.

## Features

-   **Backend:** Python FastAPI
-   **Frontend:** React with Material UI (served by FastAPI)
-   **AI Integration:**
    -   Vertex AI Gemini for ad text generation.
    -   Vertex AI Imagen for ad image generation.
-   **Deployment:** Single Docker container deployable to Google Cloud Run.

## Project Structure

```
project-alchemy-task3/
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI app, static file serving
│   │   ├── routers/ads.py      # API endpoint for ad generation
│   │   ├── services/           # Business logic (Vertex AI, prompts)
│   │   ├── models/             # Pydantic models
│   │   └── static/             # React build output served from here
│   ├── Dockerfile              # Unified Dockerfile for frontend build & backend serve
│   └── requirements.txt        # Python dependencies
├── frontend/                   # React source code (for development)
│   ├── public/
│   ├── src/                    # React components, services, etc.
│   └── package.json            # Node.js dependencies
├── scripts/
│   ├── run_local.sh            # Script to build frontend and run backend locally
│   └── deploy_cloud_run.sh     # Script to build and deploy to Cloud Run
├── .dockerignore
└── README.md
```

## Setup and Local Development

### Prerequisites

-   Node.js and npm (or yarn)
-   Python 3.10+ and pip
-   Docker
-   Google Cloud SDK (`gcloud`) configured (for deployment and Vertex AI access)

### Environment Variables

Create a `.env` file in the `project-alchemy-task3/backend/` directory for local Vertex AI configuration:

```env
# project-alchemy-task3/backend/.env
GCP_PROJECT_ID="your-gcp-project-id"
GCP_REGION="your-gcp-region" # e.g., us-central1
# GEMINI_MODEL_NAME="gemini-1.5-flash-001" # Optional: override default model
# IMAGEN_MODEL_NAME="imagegeneration@006" # Optional: override default model
# BRAND_NAME="Your Custom Brand" # Optional: override default brand name in prompts
```

Replace placeholders with your actual GCP project ID and region.

### Running Locally

1.  **Navigate to the project root:**
    ```bash
    cd project-alchemy-task3
    ```

2.  **Build Frontend and Run Backend (using script - to be created):**
    The `scripts/run_local.sh` script will automate these steps:
    *   Build the React frontend:
        ```bash
        cd frontend
        npm install
        npm run build # Output should go to backend/app/static
        cd ..
        ```
    *   Run the FastAPI backend:
        ```bash
        cd backend
        python -m venv venv
        source venv/bin/activate # On Windows: venv\Scripts\activate
        pip install -r requirements.txt
        uvicorn app.main:app --reload --port 8000
        ```
    Open your browser to `http://localhost:8000`.

    *(Alternatively, during active frontend development, you can run the React dev server (`cd frontend && npm start`) and the FastAPI server separately, ensuring CORS is configured in `backend/app/main.py` to allow requests from the React dev server's port, e.g., `http://localhost:3000`.)*

## Deployment to Google Cloud Run

1.  **Authenticate with GCP:**
    ```bash
    gcloud auth login
    gcloud config set project YOUR_GCP_PROJECT_ID
    ```

2.  **Enable necessary APIs:**
    -   Cloud Build API
    -   Artifact Registry API
    -   Cloud Run API
    -   Vertex AI API

3.  **Run the deployment script (to be created):**
    ```bash
    bash scripts/deploy_cloud_run.sh YOUR_GCP_PROJECT_ID YOUR_GCP_REGION SERVICE_NAME
    ```
    Example:
    ```bash
    bash scripts/deploy_cloud_run.sh my-gcp-project us-central1 alchemy-ad-app
    ```
    This script will:
    *   Build the Docker image using Cloud Build.
    *   Push the image to Artifact Registry.
    *   Deploy the image to Cloud Run.

## API Endpoint

-   **`POST /api/v1/generate_ad_content`**
    -   Request Body:
        ```json
        {
            "customer_type": "positive"
        }
        ```
        (or `"negative"`)
    -   Response:
        ```json
        {
            "ad_text": "Generated advertisement text...",
            "ad_image_url": "URL_to_generated_image_or_placeholder"
        }
        ```

## TODO / Future Enhancements

-   Implement actual image upload to GCS and serving via signed URLs from Imagen.
-   More sophisticated error handling and logging.
-   User authentication (if needed).
-   More detailed UI for ad display.
-   Unit and integration tests.
-   CI/CD pipeline for automated deployments.
