from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routers import ads

app = FastAPI(title="Project Alchemy Task 3 API")

# CORS Middleware (useful for local development if frontend is on a different port)
# Adjust origins as needed. For Cloud Run with integrated frontend, this might be less critical
# but good for local dev flexibility.
origins = [
    "http://localhost",
    "http://localhost:3000", # Common port for React dev server
    "http://localhost:5173", # Common port for Vite dev server
    # Add your deployed frontend URL if it's ever separate
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(ads.router, prefix="/api/v1", tags=["Advertisements"])

# Serve static files (React build)
# The 'directory' path is relative to where main.py is located.
# If React builds into 'project-alchemy-task3/backend/app/static/', this should be correct.
static_files_path = os.path.join(os.path.dirname(__file__), "static")

# Mount the 'static' directory from the React build (e.g., for JS, CSS, images within React's static folder)
# This assumes your React build process creates a 'static' subfolder for assets like CSS and JS.
# e.g., index.html might refer to <script src="/static/js/main.chunk.js"></script>
app.mount("/static", StaticFiles(directory=os.path.join(static_files_path, "static")), name="react_static_assets")

@app.get("/{catchall:path}", include_in_schema=False)
async def serve_react_app(request: Request, catchall: str):
    """
    Serve the index.html for any path not caught by API routes or specific static file mounts.
    This allows React Router to handle client-side routing.
    """
    index_file_path = os.path.join(static_files_path, "index.html")
    if os.path.exists(index_file_path):
        return FileResponse(index_file_path)
    # You could return a 404 if index.html is not found, or a more specific error.
    return FileResponse(os.path.join(os.path.dirname(__file__), "static/index.html_placeholder.html")) # Fallback if no index.html

@app.get("/", include_in_schema=False)
async def root():
    """
    Serve the index.html for the root path.
    """
    index_file_path = os.path.join(static_files_path, "index.html")
    if os.path.exists(index_file_path):
        return FileResponse(index_file_path)
    # Placeholder if index.html doesn't exist yet
    return FileResponse(os.path.join(os.path.dirname(__file__), "static/index.html_placeholder.html"))

# Placeholder index.html for initial setup until React build is integrated
# This is just to make the server runnable without the actual frontend build.
# We'll create this placeholder file next.
if not os.path.exists(os.path.join(static_files_path, "index.html_placeholder.html")):
    with open(os.path.join(static_files_path, "index.html_placeholder.html"), "w") as f:
        f.write("<html><body><h1>FastAPI Backend Running</h1><p>React frontend not built or integrated yet.</p></body></html>")

if __name__ == "__main__":
    import uvicorn
    # This is for local execution directly with `python main.py`
    # For production, Uvicorn is typically run by a process manager or Cloud Run's entrypoint.
    uvicorn.run(app, host="0.0.0.0", port=8000)
