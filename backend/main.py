import sqlite3
import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from endpoints.jobs.job_endpoints import jobs_router
from endpoints.files.file_upload_endpoints import tus_router
from services.jobs_manager import create_job_table
from settings import DBDIR

router_values = APIRouter() # Initialize the router
app = FastAPI(title="AI_doc_summarizer") # Create FastAPI app

# Database initialization
db_cnx = sqlite3.connect(DBDIR)
create_job_table(db_cnx)
db_cnx.close()

# Add the routes to the router
app.include_router(jobs_router,prefix="/jobs", tags=["Job Status"])
app.include_router(tus_router,tags=["File Upload"])

# Initialize the middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
            "Location",
            "Upload-Offset",
            "Tus-Resumable",
            "Tus-Version",
            "Tus-Extension",
            "Tus-Max-Size",
            "Upload-Expires",
            "Upload-Length",
        ],
)

# Run the app
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)